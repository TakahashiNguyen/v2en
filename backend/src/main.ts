import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { useContainer } from 'class-validator';
import { CorsOptions } from '@nestjs/common/interfaces/external/cors-options.interface';
import { NestExpressApplication } from '@nestjs/platform-express';
import { initializeTransactionalContext } from 'typeorm-transactional';

async function bootstrap() {
	initializeTransactionalContext();
	const app = await NestFactory.create<NestExpressApplication>(AppModule, {
		cors: true,
	});

	useContainer(app.select(AppModule), { fallbackOnErrors: true });
	const corsOptions: CorsOptions = {
		origin: true,
		methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
		credentials: true,
	};
	app.enableCors(corsOptions);
	app.useGlobalPipes(new ValidationPipe({}));

	await app.listen(2564, '0.0.0.0', async () => {
		console.info(`Application is running on: ${await app.getUrl()}`);
	});
}
bootstrap();
