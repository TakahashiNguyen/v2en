import { DeepPartial, FindOptionsWhere, Repository } from 'typeorm';
import { Data } from './data.entity';
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { ValidationOptions, registerDecorator } from 'class-validator';

@Injectable()
export class DataRepository {
	constructor(
		@InjectRepository(Data)
		private dataSource: Repository<Data>,
	) {}

	async findAll(): Promise<Data[]> {
		return await this.dataSource.manager.find(Data);
	}

	async findOneBy(args: FindOptionsWhere<Data>): Promise<Data | null> {
		return await this.dataSource.manager.findOneBy(Data, args);
	}

	async createData(createDataInput: DeepPartial<Data>): Promise<Data> {
		const data = this.dataSource.manager.create(Data, createDataInput);
		return await this.dataSource.manager.save(Data, data);
	}

	async removeData(arg: FindOptionsWhere<Data>): Promise<Data> {
		const data = await this.findOneBy(arg);
		await this.dataSource.manager.remove(Data, data);
		return new Data('', '', '', false);
	}

	async find(): Promise<Data[]> {
		return await this.dataSource.manager.find(Data);
	}

	async save(saveData: DeepPartial<Data>): Promise<Data> {
		return await this.dataSource.manager.save(Data, saveData);
	}

	async validate(value: string) {
		const isExited = await this.dataSource.findOneBy({ hashValue: value });
		return !isExited;
	}
}

export function IsDataExisted(validationOptions?: ValidationOptions) {
	return function (object: any, propertyName: string) {
		registerDecorator({
			name: 'IsDataExisted',
			target: object.constructor,
			propertyName: propertyName,
			options: validationOptions,
			validator: DataRepository,
		});
	};
}
