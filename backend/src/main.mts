import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module.mjs';
import { ValidationPipe } from '@nestjs/common';
import { useContainer } from 'class-validator';
import { CorsOptions } from '@nestjs/common/interfaces/external/cors-options.interface';
import { NestExpressApplication } from '@nestjs/platform-express';
import { initializeTransactionalContext } from 'typeorm-transactional';
import * as tfLib from '@tensorflow/tfjs-node-gpu';
import * as faceapiLib from '@vladmandic/face-api/dist/face-api.node-gpu.js';
import * as canvasLib from 'canvas';
import { JSDOM } from 'jsdom';

export const canvas = canvasLib;
export const faceapi = faceapiLib;
export const tf = tfLib;
export const ejs = await import('ejs');
export const dom = new JSDOM('').window;
export const modelPath = 'src/model';
export const optionsSSDMobileNet = new faceapi.SsdMobilenetv1Options({
	minConfidence: 0.5,
	maxResults: 1,
});

export async function initModels() {
	await tf.ready();
	await faceapi.nets.ssdMobilenetv1.loadFromDisk(modelPath);
	await faceapi.nets.faceLandmark68Net.loadFromDisk(modelPath);
	await faceapi.nets.faceExpressionNet.loadFromDisk(modelPath);
	await faceapi.nets.faceRecognitionNet.loadFromDisk(modelPath);
	faceapi.env.monkeyPatch({
		Canvas: dom.HTMLCanvasElement,
		FileReader: dom.FileReader,
		Image: dom.HTMLImageElement,
	});
}

export async function bootstrap() {
	initializeTransactionalContext();
	const app = await NestFactory.create<NestExpressApplication>(AppModule, {
		cors: true,
	});

	//Face authencation fix
	await initModels();
	app.setViewEngine('ejs');

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
	const dataSize = '10mb';
	app.useBodyParser('json', { limit: dataSize });

	await app.listen(2564, '0.0.0.0', async () => {
		console.info(`Application is running on: ${await app.getUrl()}`);
	});
}
