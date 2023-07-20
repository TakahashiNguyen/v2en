import {
	Entity,
	PrimaryGeneratedColumn,
	Column,
	ManyToOne,
	JoinColumn,
} from 'typeorm';
import { User } from './user.entity';
import { ObjectType } from '@nestjs/graphql';

@ObjectType()
@Entity()
export class UserSession {
	constructor(token: string, user: User) {
		this.token = token;
		this.user = user;
	}

	@PrimaryGeneratedColumn()
	id!: number;

	@Column('longtext')
	token!: string;

	@ManyToOne(() => User, (user) => user.sessions, { eager: true })
	@JoinColumn({ name: 'user_id' })
	user!: User;
}
