import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { User } from './user.entity';
import { UserResolver } from './user.resolver';
import { UserService } from './user.service';
import { IsUserNameExistedConstraint } from './user.validator';
import { UserSession } from './user.session.entity';
import { JwtModule } from '@nestjs/jwt';
import { Todo } from '../todo/todo.entity';
import { UserAuthGuard } from './user.guard';

export const jwtConstants = {
	secret: 'DO NOT USE THIS VALUE. INSTEAD, CREATE A COMPLEX SECRET AND KEEP IT SAFE OUTSIDE OF THE SOURCE CODE.',
	timeout: '120s',
};

@Module({
	providers: [
		UserResolver,
		UserService,
		IsUserNameExistedConstraint,
		UserAuthGuard,
	],
	imports: [
		TypeOrmModule.forFeature([User, UserSession]),
		JwtModule.register({
			global: true,
			secret: jwtConstants.secret,
			signOptions: {
				expiresIn: jwtConstants.timeout,
				algorithm: 'HS256',
			},
		}),
	],
	exports: [UserService, UserAuthGuard],
})
export class UserModule {}
