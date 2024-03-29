import { Module } from '@nestjs/common';
import { AppController } from './app.controller.mjs';
import { AppService } from './app.service.mjs';
import { UserModule } from './user/user.module.mjs';
import { DataModule } from './data/data.module.mjs';
import { GraphQLModule } from '@nestjs/graphql';
import { ApolloDriver, ApolloDriverConfig } from '@nestjs/apollo';
import { TypeOrmModule, TypeOrmModuleOptions } from '@nestjs/typeorm';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { join } from 'path';
import { ApolloServerPluginLandingPageLocalDefault } from '@apollo/server/plugin/landingPage/default';
import { TodoModule } from './todo/todo.module.mjs';

export const myConnectionOptions = async (
	configService: ConfigService,
): Promise<TypeOrmModuleOptions> => {
	return {
		type: 'mysql',
		host: configService.get('DB_HOST'),
		port: configService.get('DB_PORT'),
		username: configService.get('DB_USERNAME'),
		password: configService.get('DB_PASSWORD'),
		database: configService.get('DB_NAME'),
		synchronize: true,
		logging: true,
		autoLoadEntities: true,
	};
};

@Module({
	imports: [
		UserModule,
		DataModule,
		TodoModule,
		ConfigModule.forRoot({
			isGlobal: true,
		}),
		TypeOrmModule.forRootAsync({
			imports: [ConfigModule],
			useFactory: myConnectionOptions,
			inject: [ConfigService],
		}),
		GraphQLModule.forRoot<ApolloDriverConfig>({
			autoSchemaFile: join(process.cwd(), 'src/schema.gql'),
			driver: ApolloDriver,
			playground: false,
			plugins: [ApolloServerPluginLandingPageLocalDefault()],
			installSubscriptionHandlers: true,
			context: ({ req }: any) => ({ headers: req.headers }),
		}),
	],
	controllers: [AppController],
	providers: [AppService],
})
export class AppModule {}
