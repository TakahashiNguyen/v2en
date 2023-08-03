import { FindOptionsWhere, Repository } from 'typeorm';
import { User } from './user.entity.mjs';
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { UserSession } from './user.session.entity.mjs';
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

	// Section:_User
	async findAll(): Promise<User[]> {
		return await this.dataSource.find();
	}

	async findUserOneBy(args: FindOptionsWhere<User>): Promise<User | Error> {
		return (
			(await this.dataSource.findOneBy(args)) ?? new GraphQLError('User not found')
		);
	}

	async createUser(createUserInput: User): Promise<User> {
		const data = this.dataSource.create(createUserInput);
		return await this.dataSource.save(data);
	}

	async removeUser(arg: FindOptionsWhere<User>): Promise<void | Error> {
		const data = await this.findUserOneBy(arg);
		if (data instanceof User) await this.dataSource.remove(data);
		return new GraphQLError('user not found');
	}

	// Section:_UserSession
	async createSession(newSession: UserSession) {
		await this.sessionSource.save(newSession);
	}

	async findSession(args: FindOptionsWhere<UserSession>): Promise<UserSession | Error> {
		return (
			(await this.sessionSource.findOneBy(args)) ??
			new GraphQLError('Session not found')
		);
	}

	async removeSession(session: UserSession) {
		await this.sessionSource.remove(session);
	}

	// Section:_Token
	createToken(user: User) {
		return this.jwtService.sign({
			create: Date.now(),
			username: user.username,
			userStr: user.givenName + user.familyName + user.gender + user.birthDay,
			id: user.id,
		});
	}

	checkToken(token: any) {
		return this.jwtService.verify(token);
	}
}
