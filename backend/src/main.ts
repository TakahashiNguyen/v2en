import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { useContainer } from 'class-validator';

async function bootstrap() {
	const app = await NestFactory.create(AppModule, { cors: true });
	app.useGlobalPipes(new ValidationPipe({}));

	useContainer(app.select(AppModule), { fallbackOnErrors: true });

	await app.listen(3000);
	console.info(`Application is running on: ${await app.getUrl()}`);
}
bootstrap();
