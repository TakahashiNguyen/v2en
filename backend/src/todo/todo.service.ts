import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Todo } from './todo.entity';
import { FindOptionsWhere, Repository } from 'typeorm';
import { User } from 'src/user/user.entity';
import { UserService } from 'src/user/user.service';
import { GraphQLError } from 'graphql';
import { TodoObj } from './todo.dto';
import { UserSession } from 'src/user/user.session.entity';

@Injectable()
export class TodoService {
	constructor(
		@InjectRepository(Todo)
		private readonly source: Repository<Todo>,
		private readonly userService: UserService,
	) {}

	// Section: Find
	async findTodoByUser(token: string): Promise<Todo[] | Error> {
		try {
			const session = await this.userService.findSession({
				token: token,
			});
			if (session instanceof UserSession) {
				const user = await this.userService.findUserOneBy({
					id: session.user.id,
				});
				if (user instanceof User) {
					return await this.source.findBy({ user: user });
				} else throw user;
			} else throw session;
		} catch (error) {
			if (error instanceof Error) return error;
		}
		return new GraphQLError('Something went wrong');
	}

	async findTodoOneBy(args: FindOptionsWhere<Todo>): Promise<Todo | Error> {
		return (
			(await this.source.findOneBy(args)) ??
			new GraphQLError('Todo not found')
		);
	}

	// Section: Editor
	async createTodo(
		createTodoInput: TodoObj,
		token: string,
	): Promise<Todo | Error> {
		try {
			const session = await this.userService.findSession({
				token: token,
			});
			if (session instanceof UserSession) {
				const user = await this.userService.findUserOneBy(session.user);
				if (user instanceof User) {
					const todo = Todo.fromInput(createTodoInput, user);
					if ((await this.findTodoOneBy(todo)) instanceof Error)
						return await this.source.save(this.source.create(todo));
					return new GraphQLError('Todo already existed');
				} else throw user;
			} else throw session;
		} catch (err) {
			if (err instanceof Error) return err;
		}
		return new GraphQLError('Something went wrong');
	}

	async removeTodo(arg: FindOptionsWhere<Todo>): Promise<void | Error> {
		const data = await this.findTodoOneBy(arg);
		if (data instanceof Error) return data;
		await this.source.remove(data);
	}
}
