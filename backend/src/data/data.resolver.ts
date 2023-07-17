import { Args, Mutation, Query, Resolver, Subscription } from '@nestjs/graphql';
import { DataService } from './data.service';
import { Data } from './data.entity';
import { PubSub } from 'graphql-subscriptions';
import { DataInput } from './data.dto';
import { GraphQLError } from 'graphql';
import { UseGuards } from '@nestjs/common';
import { AuthGuard } from 'src/user/auth.guard';

const pubSub = new PubSub();

@Resolver(() => Data)
export class DataResolver {
	constructor(private readonly dataService: DataService) {}

	// Queries:Section: Data
	@Query(() => [Data])
	@UseGuards(AuthGuard)
	datas(): Promise<Data[]> {
		return this.dataService.findDataAll();
	}

	@Query(() => Data)
	@UseGuards(AuthGuard)
	async data(@Args('id') id: number): Promise<Data | Error> {
		return await this.dataService.findDataOneBy({ id: id });
	}

	// Mutations:Section: Data
	@Mutation(() => Data)
	@UseGuards(AuthGuard)
	async addData(
		@Args('newData') newData: DataInput,
		id?: number,
	): Promise<Data | unknown> {
		let data = await Data.fromDataInput(newData, id);
		if (
			(await this.dataService.findDataOneBy({
				hashValue: data.hashValue,
			})) instanceof Error
		) {
			data = await this.dataService.createData(data);
			pubSub.publish('dataAdded', { dataAdded: data });
			return data;
		}
		return new GraphQLError('Data already existed');
	}

	@Mutation(() => String)
	@UseGuards(AuthGuard)
	async removeData(@Args('id') id: number) {
		const data = await this.dataService.findDataOneBy({ id: id });
		if (data instanceof Data) {
			await this.dataService.removeData({ hashValue: data.hashValue });
			return 'Data removed';
		} else return new GraphQLError("Data isn't existed");
	}

	@Mutation(() => String)
	@UseGuards(AuthGuard)
	async modifyData(
		@Args('id') id: number,
		@Args('newData') newData: DataInput,
	) {
		await this.removeData(id);
		await this.addData(newData, id);
		return 'Data modified';
	}
}
