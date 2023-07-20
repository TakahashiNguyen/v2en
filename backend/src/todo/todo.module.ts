import { Module } from '@nestjs/common';
import { TodoResolver } from './todo.resolver';
import { TodoService } from './todo.service';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Todo } from './todo.entity';
import { UserModule } from '../user/user.module';

@Module({
	imports: [TypeOrmModule.forFeature([Todo]), UserModule],
	providers: [TodoResolver, TodoService],
})
export class TodoModule {}
