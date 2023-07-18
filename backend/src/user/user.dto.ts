import { Field, InputType, ObjectType } from '@nestjs/graphql';
import { User } from './user.entity';
import { Entity } from 'typeorm';
import { IsPasswordCorrent, IsUserNameExisted } from './user.validator';

@InputType('UserInput')
export class UserInput {
	constructor(
		username = '',
		familyName = '',
		givenName = '',
		gender = '',
		password = Math.random().toString(36).substring(2, 18),
		birthDay: Date = new Date('1999-12-31'),
	) {
		this.username = username;
		this.familyName = familyName;
		this.givenName = givenName;
		this.gender = gender;
		this.birthDay = birthDay;
		this.password = password;
	}

	@IsUserNameExisted({ message: 'username is existed' })
	@Field(() => String, { nullable: false })
	username: string;

	@Field(() => String, { nullable: false })
	familyName: string;

	@Field(() => String, { nullable: false })
	givenName: string;

	private _birthDay?: string;
	@Field(() => Date)
	get birthDay(): string {
		return this._birthDay ?? '1999-12-31';
	}
	set birthDay(value: Date) {
		this._birthDay = value.toISOString().substring(0, 10);
	}

	@Field(() => String, { nullable: false })
	gender?: string;

	@IsPasswordCorrent({
		message:
			'The password must have the minimum length 8 with at leat a special character and more than 3 number',
	})
	@Field(() => String, { nullable: false })
	password?: string;
}

@InputType('LoginInput')
export class LoginInput {
	constructor(username = '', password = '') {
		this.username = username;
		this.password = password;
	}

	static fromUserInput(user: UserInput) {
		return new LoginInput(user.username, user.password);
	}

	@Field(() => String, { nullable: false })
	username: string;

	@IsPasswordCorrent({
		message:
			'The password must have the minimum length 8 with at leat a special character and more than 3 number',
	})
	@Field(() => String, { nullable: false })
	password: string;
}

@Entity()
@ObjectType('UserOutput')
export class UserOutput {
	constructor(
		username = '',
		familyName = '',
		givenName = '',
		gender = '',
		birthDay: Date = new Date(0, 0, 0),
		token: string = '',
	) {
		this.username = username;
		this.familyName = familyName;
		this.givenName = givenName;
		this.gender = gender;
		this.birthDay = birthDay;
		this.token = token;
	}

	static fromUser(user: User, token?: string) {
		return new UserOutput(
			user.username,
			user.familyName,
			user.givenName,
			user.gender,
			new Date(user.birthDay ?? '2000-01-01'),
			token,
		);
	}

	@Field()
	username: string;

	@Field()
	familyName: string;

	@Field()
	givenName: string;

	@Field()
	gender: string;

	@Field()
	birthDay: Date;

	@Field()
	token: string;
}
