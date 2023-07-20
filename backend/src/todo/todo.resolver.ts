import { Args, Resolver, Query, Mutation, Context } from '@nestjs/graphql';
import { TodoService } from './todo.service';
import { UseGuards } from '@nestjs/common';
import { Todo } from './todo.entity';
import { UserAuthGuard } from 'src/user/user.guard';
import { TodoObj } from './todo.dto';

@Resolver(() => Todo)
export class TodoResolver {
	constructor(private readonly service: TodoService) {}

	// Queries:Section: Todo
	@Query(() => [TodoObj])
	@UseGuards(UserAuthGuard)
	async todos(
		obj: any,
		args: any,
		context: any,
		info: any,
	): Promise<Todo[] | Error> {
		const token = context.req.headers.authorization.split(' ')[1];
		return await this.service.findTodoByUser(token);
	}

	// Mutations:Section: Todo
	@Mutation(() => TodoObj)
	@UseGuards(UserAuthGuard)
	async addTodo(
		@Args('newTodo') newTodo: TodoObj,
		@Context('headers') headers: any,
	): Promise<TodoObj | Error> {
		const token = headers.authorization.split(' ')[1];
		return await this.service.createTodo(newTodo, token);
	}
}
