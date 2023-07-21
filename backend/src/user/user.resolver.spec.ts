import { Test, TestingModule } from '@nestjs/testing';
import { AppModule } from '../app.module';
import { UserResolver } from './user.resolver';
import { LoginInput, UserInput } from './user.dto';

const username = Math.random().toString(36).substring(2, 10);
const firstname = Math.random().toString(36).substring(2, 10);
const lastname = Math.random().toString(36).substring(2, 10);
const password = Math.random().toString(36).substring(2, 10);
let token: string | Error;

describe('UserResolver', () => {
	let resolver: UserResolver;
	// Section:Define:
	beforeEach(async () => {
		const module: TestingModule = await Test.createTestingModule({
			imports: [AppModule],
		}).compile();

		resolver = module.get<UserResolver>(UserResolver);
	});

	it('should be defined', () => {
		expect(resolver).toBeDefined();
	});
	// Section:Test:
	describe('User', () => {
		it('Sign up', async () => {
			token = await resolver.addUser(
				new UserInput(
					username,
					firstname,
					lastname,
					'',
					password,
					new Date('2006-02-06'),
				),
			);

			expect(typeof token).toMatch('string');
		});

		test('Log in', async () => {
			token = await resolver.LogIn(new LoginInput(username, password));

			expect(typeof token).toMatch('string');
		});

		it('Log out', async () => {
			let msg = await resolver.LogOut(
				username,
				typeof token === 'string' ? token : '',
			);

			expect(msg).toMatch('User logged out');
		});
	});
});
