import { Entity, PrimaryGeneratedColumn, Column, ManyToOne, JoinColumn } from 'typeorm';
import { User } from './user.entity.mjs';
import { ObjectType } from '@nestjs/graphql';

@ObjectType()
@Entity()
export class UserSession {
	constructor(token: string, user: Awaited<User>) {
		this.token = token;
		this.user = user;
	}

	@PrimaryGeneratedColumn()
	id!: number;

	@Column('longtext')
	token!: string;

	@ManyToOne(() => User, (user) => user.sessions, { eager: true })
	@JoinColumn({ name: 'userID' })
	user!: Awaited<User>;
}
