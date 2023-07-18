import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { User } from './user.entity';
import { UserResolver } from './user.resolver';
import { UserService } from './user.service';
import { IsUserNameExistedConstraint } from './user.validator';
import { Session } from './session.entity';
import { JwtModule } from '@nestjs/jwt';

export const jwtConstants = {
	secret: 'DO NOT USE THIS VALUE. INSTEAD, CREATE A COMPLEX SECRET AND KEEP IT SAFE OUTSIDE OF THE SOURCE CODE.',
	timeout: '120s',
};

@Module({
	providers: [UserResolver, UserService, IsUserNameExistedConstraint],
	imports: [
		TypeOrmModule.forFeature([User, Session]),
		JwtModule.register({
			global: true,
			secret: jwtConstants.secret,
			signOptions: {
				expiresIn: jwtConstants.timeout,
				algorithm: 'HS256',
			},
		}),
	],
})
export class UserModule {}
