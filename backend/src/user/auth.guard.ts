import {
	ExecutionContext,
	Inject,
	Injectable,
	forwardRef,
} from '@nestjs/common';
import { GqlExecutionContext } from '@nestjs/graphql';
import { AuthGuard as NestAuthGuard } from '@nestjs/passport';
import { UserService } from './user.service';

@Injectable()
export class AuthGuard extends NestAuthGuard('jwt') {
	constructor(
		@Inject(forwardRef(() => UserService))
		private readonly service: UserService,
	) {
		super();
	}

	canActivate(context: ExecutionContext) {
		const ctx = GqlExecutionContext.create(context);
		const { req } = ctx.getContext();
		if (req.headers.authorization)
			return this.service.checkToken(
				req.headers.authorization.split(' ')[1],
			);
		return false;
	}
}
