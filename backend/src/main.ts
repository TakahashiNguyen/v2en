import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { useContainer } from 'class-validator';
import { CorsOptions } from '@nestjs/common/interfaces/external/cors-options.interface';
import { NestExpressApplication } from '@nestjs/platform-express';
import { initializeTransactionalContext } from 'typeorm-transactional';
import * as bodyParser from 'body-parser';
import * as faceapi from 'face-api.js';
import { JSDOM } from 'jsdom';

export const dom = new JSDOM('').window;
async function bootstrap() {
	initializeTransactionalContext();
	const app = await NestFactory.create<NestExpressApplication>(AppModule, {
		cors: true,
	});

	//face-api.js init
	await faceapi.loadFaceDetectionModel(
		'https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/ssd_mobilenetv1_model-weights_manifest.json',
	);

	//Image DOM element load
	faceapi.env.monkeyPatch({
		Image: dom.HTMLImageElement,
	});

	//CORS fix
	useContainer(app.select(AppModule), { fallbackOnErrors: true });
	const corsOptions: CorsOptions = {
		origin: true,
		methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
		credentials: true,
	};
	app.enableCors(corsOptions);
	app.useGlobalPipes(new ValidationPipe({}));

	//Allow large request
	const dataSize = '25mb';
	app.use(bodyParser.json({ limit: dataSize }));
	app.use(bodyParser.urlencoded({ limit: dataSize, extended: true }));

	await app.listen(2564, '0.0.0.0', async () => {
		console.info(`Application is running on: ${await app.getUrl()}`);
	});
}
bootstrap();
