import { Args, Mutation, Query, Resolver } from '@nestjs/graphql';
import { DataService } from './data.service';
import { Data } from './data.entity';
import { DataInput } from './data.dto';
import { GraphQLError } from 'graphql';
import { UseGuards } from '@nestjs/common';
import { UserAuthGuard } from '../user/user.guard';

@Resolver(() => Data)
export class DataResolver {
	constructor(private readonly dataService: DataService) {}

	// Queries:Section:_Data
	@Query(() => [Data])
	@UseGuards(UserAuthGuard)
	datas(): Promise<Data[]> {
		return this.dataService.findDataAll();
	}

	@Query(() => Data)
	@UseGuards(UserAuthGuard)
	async data(@Args('id') id: string): Promise<Data | Error> {
		return await this.dataService.findDataOneBy({ id: id });
	}

	// Mutations:Section:_Data
	@Mutation(() => Data)
	@UseGuards(UserAuthGuard)
	async addData(
		@Args('newData') newData: DataInput,
		id?: string,
	): Promise<Data | Error> {
		let data = await Data.fromDataInput(newData, id);
		if (
			(await this.dataService.findDataOneBy({
				hashValue: data.hashValue,
			})) instanceof Error
		) {
			return await this.dataService.createData(data);
		}
		return new GraphQLError('Data already existed');
	}

	@Mutation(() => String)
	@UseGuards(UserAuthGuard)
	async removeData(@Args('id') id: string) {
		const data = await this.dataService.findDataOneBy({ id: id });
		if (data instanceof Data) {
			await this.dataService.removeData({ hashValue: data.hashValue });
			return 'Data removed';
		} else return new GraphQLError("Data isn't existed");
	}

	@Mutation(() => String)
	@UseGuards(UserAuthGuard)
	async modifyData(
		@Args('id') id: string,
		@Args('newData') newData: DataInput,
	) {
		await this.removeData(id);
		await this.addData(newData, id);
		return 'Data modified';
	}
}
