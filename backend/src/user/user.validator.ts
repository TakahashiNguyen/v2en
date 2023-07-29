import { Injectable } from '@nestjs/common';
import {
	ValidationOptions,
	ValidatorConstraint,
	ValidatorConstraintInterface,
	registerDecorator,
} from 'class-validator';
import { UserService } from './user.service';
import { User } from './user.entity';

export function IsUserNameExisted(validationOptions?: ValidationOptions) {
	return function (object: any, propertyName: string) {
		registerDecorator({
			target: object.constructor,
			propertyName,
			options: validationOptions,
			validator: IsUserNameExistedConstraint,
		});
	};
}

@ValidatorConstraint({ async: true })
@Injectable()
export class IsUserNameExistedConstraint
	implements ValidatorConstraintInterface
{
	constructor(private readonly userService: UserService) {}

	async validate(value: any): Promise<boolean> {
		return !(
			(await this.userService.findUserOneBy({
				username: value,
			})) instanceof User
		);
	}
}

export function IsPasswordCorrent(validationOptions?: ValidationOptions) {
	return function (object: any, propertyName: string) {
		registerDecorator({
			target: object.constructor,
			propertyName,
			options: validationOptions,
			validator: IsPasswordCorrentConstraint,
		});
	};
}

@ValidatorConstraint({ async: true })
export class IsPasswordCorrentConstraint
	implements ValidatorConstraintInterface
{
	constructor() {}

	async validate(value: string): Promise<boolean> {
		if (value.split(' ').length > 2) return false;
		const type = value.split(' ')[0];
		const password = value.split(' ')[1];
		if (
			type != 'UserPasswordAuthencation' &&
			type != 'UserFaceAuthencation'
		)
			return false;
		return (
			password.length >= 8 && password.replace(/[^0-9]/g, '').length > 3
		);
	}
}
