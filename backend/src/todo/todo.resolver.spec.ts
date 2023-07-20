import { Test, TestingModule } from '@nestjs/testing';
import { TodoResolver } from './todo.resolver';
import { AppModule } from 'src/app.module';

describe('TodoResolver', () => {
	let resolver: TodoResolver;

	beforeEach(async () => {
		const module: TestingModule = await Test.createTestingModule({
			imports: [AppModule],
		}).compile();

		resolver = module.get<TodoResolver>(TodoResolver);
	});

	it('should be defined', () => {
		expect(resolver).toBeDefined();
	});
});
