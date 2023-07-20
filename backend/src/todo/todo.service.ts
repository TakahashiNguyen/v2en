import { Inject, Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Todo } from './todo.entity';
import { FindOptionsWhere, Repository } from 'typeorm';
import { User } from 'src/user/user.entity';
import { UserService } from 'src/user/user.service';
import { GraphQLError } from 'graphql';

@Injectable()
export class TodoService {
	constructor(
		@InjectRepository(Todo)
		private source: Repository<Todo>,
		@Inject(UserService)
		private readonly userService: UserService,
	) {}

	// Section: Find
	async findTodoByUserID(
		userArgs: FindOptionsWhere<User>,
	): Promise<Todo[] | Error> {
		const user = await this.userService.findUserOneBy(userArgs);
		if (user instanceof User)
			return await this.source.findBy({ user: user });
		return user;
	}

	async findTodoOneBy(args: FindOptionsWhere<Todo>): Promise<Todo | Error> {
		return (
			(await this.source.findOneBy(args)) ??
			new GraphQLError('Todo not found')
		);
	}

	// Section: Editor
	async createTodo(createTodoInput: Todo): Promise<Todo> {
		const data = this.source.create(createTodoInput);
		return await this.source.save(data);
	}

	async removeTodo(arg: FindOptionsWhere<Todo>): Promise<void | Error> {
		const data = await this.findTodoOneBy(arg);
		if (data instanceof Error) return data;
		await this.source.remove(data);
	}
}
