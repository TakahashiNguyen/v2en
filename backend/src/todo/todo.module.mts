import { Module } from '@nestjs/common';
import { TodoResolver } from './todo.resolver.mjs';
import { TodoService } from './todo.service.mjs';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Todo } from './todo.entity.mjs';
import { UserModule } from '../user/user.module.mjs';

@Module({
	imports: [TypeOrmModule.forFeature([Todo]), UserModule],
	providers: [TodoResolver, TodoService],
})
export class TodoModule {}
