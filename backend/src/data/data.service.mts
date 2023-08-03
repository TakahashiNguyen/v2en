import { FindOptionsWhere, Repository } from 'typeorm';
import { Data } from './data.entity.mjs';
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { GraphQLError } from 'graphql';

@Injectable()
export class DataService {
	constructor(
		@InjectRepository(Data)
		private source: Repository<Data>,
	) {}

	// Section:_Find
	async findDataAll(): Promise<Data[]> {
		return await this.source.find();
	}

	async findDataOneBy(args: FindOptionsWhere<Data>): Promise<Data | Error> {
		return (await this.source.findOneBy(args)) ?? new GraphQLError('Data not found');
	}

	// Section:_Editor
	async createData(createDataInput: Data): Promise<Data> {
		const data = this.source.create(createDataInput);
		return await this.source.save(data);
	}

	async removeData(arg: FindOptionsWhere<Data>): Promise<void | Error> {
		const data = await this.findDataOneBy(arg);
		if (data instanceof Error) return data;
		await this.source.remove(data);
	}
}
