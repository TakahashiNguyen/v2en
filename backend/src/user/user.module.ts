import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { User } from './user.entity';
import { UserResolver } from './user.resolver';
import { UserService } from './user.service';
import { UserSession } from './user.session.entity';
import { JwtModule } from '@nestjs/jwt';
import { UserAuthGuard } from './user.guard';
import { IsUserNameExistedConstraint } from './user.validator';

export const jwtConstants = {
	secret: 'DO NOT USE THIS VALUE. INSTEAD, CREATE A COMPLEX SECRET AND KEEP IT SAFE OUTSIDE OF THE SOURCE CODE.',
	timeout: '120s',
};

@Module({
	providers: [
		UserResolver,
		UserService,
		UserAuthGuard,
		IsUserNameExistedConstraint,
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
