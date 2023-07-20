import { FindOptionsWhere, Repository } from 'typeorm';
import { User } from './user.entity';
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { UserSession } from './user.session.entity';
import { JwtService } from '@nestjs/jwt';
import { GraphQLError } from 'graphql';

@Injectable()
export class UserService {
	constructor(
		@InjectRepository(User)
		private dataSource: Repository<User>,
		@InjectRepository(UserSession)
		private sessionSource: Repository<UserSession>,
		private jwtService: JwtService,
	) {}

	// Section: User
	async findAll(): Promise<User[]> {
		return await this.dataSource.find();
	}

	async findUserOneBy(args: FindOptionsWhere<User>): Promise<User | Error> {
		return (
			(await this.dataSource.manager.findOneBy(User, args)) ??
			new GraphQLError('User not found')
		);
	}

	async createUser(createUserInput: User): Promise<User> {
		const data = this.dataSource.manager.create(User, createUserInput);
		return await this.dataSource.manager.save(User, data);
	}

	async removeUser(arg: FindOptionsWhere<User>): Promise<void> {
		const data = await this.findUserOneBy(arg);
		await this.dataSource.manager.remove(User, data);
	}

	// Section: UserSession
	async createSession(newSession: UserSession) {
		await this.sessionSource.manager.save(UserSession, newSession);
	}

	async findSession(args: FindOptionsWhere<UserSession>) {
		return await this.sessionSource.manager.findOneBy(UserSession, args);
	}

	async removeSession(session: UserSession) {
		await this.sessionSource.manager.remove(UserSession, session);
	}

	// Section: Token
	createToken(user: User) {
		return this.jwtService.sign({
			create: Date.now(),
			username: user.username,
			userStr:
				user.givenName + user.familyName + user.gender + user.birthDay,
			id: user.id,
		});
	}

	checkToken(token: any) {
		return this.jwtService.verify(token);
	}
}
