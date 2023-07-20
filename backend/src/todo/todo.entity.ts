import { ObjectType } from '@nestjs/graphql';
import { User } from 'src/user/user.entity';
import {
	Column,
	Entity,
	JoinColumn,
	ManyToOne,
	PrimaryGeneratedColumn,
} from 'typeorm';

@ObjectType()
@Entity()
export class Todo {
	@PrimaryGeneratedColumn('uuid')
	id!: number;

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
