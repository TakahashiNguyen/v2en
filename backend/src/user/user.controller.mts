import { Controller, Get, Res } from '@nestjs/common';
import { Response } from 'express';
import { dom, ejs } from '../main.mjs';

@Controller('user')
export class UserController {
	@Get('image')
	async getBrowserSite(@Res() res: Response) {
		const img = new dom.Image();
		img.onload = () => {
			console.log('Image loaded');
		};
		img.src =
			'data:image/jpeg;base64,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';
		const html = ejs.render(
			'<h1>Welcome to <%= title %>!<img src="<%= imageSrc %>" /></h1>',
			{
				title: 'My Site',
				imageSrc: img.src,
			},
		);
		res.send(html);
	}
}
