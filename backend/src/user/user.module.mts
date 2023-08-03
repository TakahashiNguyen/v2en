import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { User } from './user.entity.mjs';
import { UserResolver } from './user.resolver.mjs';
import { UserService } from './user.service.mjs';
import { UserSession } from './user.session.entity.mjs';
import { JwtModule } from '@nestjs/jwt';
import { UserAuthGuard } from './user.guard.mjs';
import { IsUserNameExistedConstraint } from './user.validator.mjs';
import { UserController } from './user.controller.mjs';

export const jwtConstants = {
	secret: 'DO NOT USE THIS VALUE. INSTEAD, CREATE A COMPLEX SECRET AND KEEP IT SAFE OUTSIDE OF THE SOURCE CODE.',
	timeout: '120s',
};

@Module({
	providers: [UserResolver, UserService, UserAuthGuard, IsUserNameExistedConstraint],
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
	controllers: [UserController],
})
export class UserModule {}
