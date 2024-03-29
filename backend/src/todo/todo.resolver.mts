import { Args, Resolver, Query, Mutation, Context } from '@nestjs/graphql';
import { TodoService } from './todo.service.mjs';
import { UseGuards } from '@nestjs/common';
import { Todo } from './todo.entity.mjs';
import { UserAuthGuard } from '../user/user.guard.mjs';
import { TodoObj } from './todo.dto.mjs';

@Resolver(() => Todo)
export class TodoResolver {
	constructor(private readonly service: TodoService) {}

	// Queries:Section:_Todo
	@Query(() => [TodoObj])
	@UseGuards(UserAuthGuard)
	async todos(@Context('headers') headers: any): Promise<Todo[] | Error> {
		return await this.service.findTodoByUser(headers.authorization.split(' ')[1]);
	}

	// Mutations:Section:_Todo
	@Mutation(() => TodoObj)
	@UseGuards(UserAuthGuard)
	async addTodo(
		@Args('newTodo') newTodo: TodoObj,
		@Context('headers') headers: any,
	): Promise<Todo | Error> {
		return await this.service.createTodo(
			newTodo,
			headers.authorization.split(' ')[1],
		);
	}

	@Mutation(() => String)
	@UseGuards(UserAuthGuard)
	async removeTodo(
		@Args('todoID') todoID: string,
		@Context('headers') headers: any,
	): Promise<string | Error> {
		return await this.service.removeTodo(todoID, headers.authorization.split(' ')[1]);
	}

	@Mutation(() => String)
	@UseGuards(UserAuthGuard)
	async updateTodo(
		@Args('todoID') todoID: string,
		@Context('headers') headers: any,
	): Promise<string | Error> {
		await this.service.updateTodo(todoID, headers.authorization.split(' ')[1]);
		return 'success';
	}
}
