import { Repository } from 'typeorm';
import { UserService } from './user.service';
import { User } from './user.entity';
import { Test, TestingModule } from '@nestjs/testing';
import { getRepositoryToken } from '@nestjs/typeorm';
import { AppModule } from '../app.module';

describe('UserService', () => {
	let service: UserService;
	let repository: Repository<User>;

	beforeEach(async () => {
		const module: TestingModule = await Test.createTestingModule({
			imports: [AppModule],
		}).compile();

		service = module.get<UserService>(UserService);
		repository = module.get<Repository<User>>(getRepositoryToken(User));
	});

	it('should be defined', () => {
		expect(service).toBeDefined();
	});

	describe('Method findAll', () => {
		it('it should return 2 items', async () => {
			jest.spyOn(repository, 'find').mockResolvedValueOnce(ITEMS);
			const result = await service.findAll();
			expect(result.length).toEqual(2);
		});
	});
});

const ITEMS: User[] = [
	{
		id: 1,
		username: 'dahfiuahfoiudsahdfoiu',
		familyName: 'lmao',
		givenName: 'bruh',
		hashedPassword: 'iufdaoifugaoifugdsaoifhua',
		password: 'oiudgasfoigdafoiag',
	},
	{
		id: 2,
		username: 'dahfiuaqerqerhfoiudsahdfoiu',
		familyName: 'lmao',
		givenName: 'bruh',
		hashedPassword: 'iufdaoifugaoifugdsaoifhua',
		password: 'oiudgasfoigdafoiag',
	},
];
