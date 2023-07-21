import { ObjectType } from '@nestjs/graphql';
import { Md5 } from 'ts-md5';
import { Column, Entity, PrimaryGeneratedColumn } from 'typeorm';
import { DataInput } from './data.dto';

@Entity()
@ObjectType()
export class Data {
	constructor(
		origin = '',
		translated = '',
		translator = '',
		verified = false,
		id?: string,
	) {
		this.id = id;
		this.origin = origin;
		this.translated = translated;
		this.translator = translator;
		this.verified = verified;
	}

	static async fromDataInput(data: DataInput, id?: string) {
		return new Data(
			data.origin,
			data.translated,
			data.translator,
			data.verified,
			id,
		);
	}

	@PrimaryGeneratedColumn('uuid')
	id?: string;

	@Column('longtext')
	origin: string;

	@Column('longtext')
	translated: string;

	@Column('longtext')
	translator: string;

	@Column('longtext', { nullable: false })
	get hashValue(): string {
		return Md5.hashStr(
			`${this.origin} ${this.translated} ${this.translator}`,
		).toString();
	}
	set hashValue(value: string) {
		value;
	}

	@Column({ default: false })
	verified: boolean;
}
