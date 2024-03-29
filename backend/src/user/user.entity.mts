import { ObjectType } from '@nestjs/graphql';
import { Md5 } from 'ts-md5';
import { Column, Entity, JoinColumn, OneToMany, PrimaryGeneratedColumn } from 'typeorm';
import { UserInput } from './user.dto.mjs';
import { UserSession } from './user.session.entity.mjs';
import { Todo } from '../todo/todo.entity.mjs';

@ObjectType('UserObject')
@Entity()
export class User {
	constructor(
		username = '',
		familyName = '',
		givenName = '',
		gender = '',
		birthDay: string = new Date(0, 0, 0).toISOString(),
		password = '',
		userFace = '',
	) {
		this.username = username;
		this.familyName = familyName;
		this.givenName = givenName;
		this.password = password;
		this.gender = gender;
		this.birthDay = birthDay;
		this.userFace = userFace;
	}

	static fromUserInput(user: UserInput) {
		return new User(
			user.username,
			user.familyName,
			user.givenName,
			user.gender,
			user.birthDay,
			user.password.split(' ')[1],
			user.userFace,
		);
	}

	@PrimaryGeneratedColumn('uuid')
	id!: number;

	@Column('text')
	username: string;

	@Column('text')
	familyName: string;

	@Column('text')
	givenName: string;

	@Column('date')
	birthDay: string;

	@Column('text')
	gender: string;

	@Column('longtext')
	userFace: string;

	@Column('text')
	hashedPassword!: string;
	set password(value: string) {
		this.hashedPassword = Md5.hashStr(value);
	}

	@OneToMany(() => UserSession, (session) => session.user, { cascade: true })
	@JoinColumn({ name: 'userID' })
	sessions?: UserSession[];

	@OneToMany(() => Todo, (todo) => todo.user, { cascade: true })
	@JoinColumn({ name: 'userTodoList' })
	todoList?: Todo[];
}
