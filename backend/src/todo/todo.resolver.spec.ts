import { Test, TestingModule } from '@nestjs/testing';
import { TodoResolver } from './todo.resolver.mjs';
import { AppModule } from '../app.module.mjs';

const username = Math.random().toString(36).substring(2, 10);
const firstname = Math.random().toString(36).substring(2, 10);
const lastname = Math.random().toString(36).substring(2, 10);
const password = Math.random().toString(36).substring(2, 10);
let token: string | Error;

describe('TodoResolver', () => {
	let resolver: TodoResolver;
	// Section:Define:
	beforeEach(async () => {
		const module: TestingModule = await Test.createTestingModule({
			imports: [AppModule],
		}).compile();

		resolver = module.get<TodoResolver>(TodoResolver);
	});

	it('should be defined', () => {
		expect(resolver).toBeDefined();
	});
	// Section:Test:
	describe('Todo', () => {});
});
