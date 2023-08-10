import { Args, Mutation, Resolver } from "@nestjs/graphql";
import { User } from "./user.entity.mjs";
import { UserService } from "./user.service.mjs";
import { LoginInput, UserInput, UserOutput } from "./user.dto.mjs";
import { Md5 } from "ts-md5";
import { UserSession } from "./user.session.entity.mjs";
const { TokenExpiredError } = await import("jsonwebtoken");
import { GraphQLError } from "graphql";
import { jsdom, faceapi, optionsSSDMobileNet, vConsole, tf } from "../main.mjs";

async function faceDescriptor(input: string) {
	return await faceapi
		.detectSingleFace(await faceapi.fetchBase64(input), optionsSSDMobileNet)
		.withFaceLandmarks()
		.withFaceDescriptor()
		.run();
}

@Resolver(() => UserOutput)
export class UserResolver {
	constructor(private readonly service: UserService) {}

	// Section:Mutations:_User
	@Mutation(() => String)
	async addUser(@Args("newUser") newUser: UserInput): Promise<string | Error> {
		await this.service.createUser(User.fromUserInput(newUser));
		return await this.LogIn(LoginInput.fromUserInput(newUser));
	}

	@Mutation(() => String)
	async LogIn(@Args("loginUser") loginUser: LoginInput): Promise<string | Error> {
		const type = loginUser.password.split(" ")[0];
		const password = loginUser.password.split(" ")[1];
		let user: User | Error = new GraphQLError("Incorrect username or password.");
		if (type == "UserPasswordAuthencation")
			user = await this.service.findUserOneBy({
				username: loginUser.username,
				hashedPassword: Md5.hashStr(password),
			});
		else if (type == "UserFaceAuthencation") {
			let user: User | Error = await this.service.findUserOneBy({
				username: loginUser.username,
			});
			if (user instanceof Error)
				return new GraphQLError("Incorrect username or password.");
			const input = await faceDescriptor(password);
			const origin = await faceDescriptor(user.userFace);

			return new GraphQLError("Face Recognization has error");
		}
		if (user instanceof User) {
			const token = this.service.createToken(user);
			const session = new UserSession(token, user);
			await this.service.createSession(session);
			return token;
		}
		return user;
	}

	@Mutation(() => String)
	async LogOut(
		@Args("username") username: string,
		@Args("token") token: string,
	): Promise<String | Error> {
		try {
			const user = await this.service.findUserOneBy({
				username: username,
			});
			if (user instanceof User) {
				const session = await this.service.findSession({
					user: user,
					token: token,
				});
				if (session instanceof UserSession) {
					await this.service.removeSession(session);
					return "User logged out";
				} else throw session;
			} else throw user;
		} catch (error) {
			if (error instanceof Error) return error;
		}
		return new GraphQLError("User already logged out.");
	}

	// Section:Mutations:_Token
	@Mutation(() => UserOutput)
	async checkToken(@Args("token") token: string): Promise<UserOutput | Error> {
		try {
			const session = await this.service.findSession({ token: token });
			if (session instanceof UserSession) {
				const user = await this.service.findUserOneBy({
					id: session.user.id,
				});
				if (user instanceof User) {
					try {
						this.service.checkToken(token);
					} catch (err) {
						if (err instanceof TokenExpiredError) {
							this.service.removeSession(session);
							token = this.service.createToken(user);
							await this.service.createSession(
								new UserSession(token, user),
							);
						} else {
							return new GraphQLError(
								"Error while verifying token: " + err,
							);
						}
					}
					return UserOutput.fromUser(user, token);
				} else throw user;
			} else throw session;
		} catch (error) {
			if (error instanceof Error) return error;
		}
		return new GraphQLError("Something went wrong");
	}
}
