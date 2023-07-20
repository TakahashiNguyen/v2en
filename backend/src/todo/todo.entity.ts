import { ObjectType } from '@nestjs/graphql';
import { User } from '../user/user.entity';
import {
	Column,
	Entity,
	JoinColumn,
	ManyToOne,
	PrimaryGeneratedColumn,
} from 'typeorm';
import { TodoObj } from './todo.dto';

@ObjectType()
@Entity()
export class Todo {
	constructor(
		jobDescription: string = '',
		deadline: Date = new Date('1890-05-19'),
		finished: boolean = false,
		user: User = new User(),
	) {
		this.jobDescription = jobDescription;
		this.deadline = deadline;
		this.finished = finished;
		this.user = user;
	}

	static fromInput(todo: TodoObj, user: User) {
		return new Todo(
			todo.jobDescription,
			todo.deadline,
			todo.finished,
			user,
		);
	}

	@PrimaryGeneratedColumn('uuid')
	id!: string;

	@Column('longtext')
	jobDescription!: string;

	@Column({ type: 'timestamp', default: () => 'CURRENT_TIMESTAMP' })
	deadline!: Date;

	@Column('boolean')
	finished: boolean = false;

	@ManyToOne(() => User, (user) => user.todoList, { eager: true })
	@JoinColumn({ name: 'userTodoList' })
	user!: User;
}
