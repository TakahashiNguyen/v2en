import { ObjectType } from '@nestjs/graphql';
import { Md5 } from 'ts-md5';
import { Column, Entity, PrimaryColumn, PrimaryGeneratedColumn } from 'typeorm';
import { DataInput } from './data.dto';
import { Injectable } from '@nestjs/common';

@Entity()
@ObjectType('DataObject')
@Injectable()
export class Data {
	constructor(
		origin = '',
		translated = '',
		translator = '',
		verified = false,
		id?: number,
	) {
		this.id = id;
		this.origin = origin;
		this.translated = translated;
		this.translator = translator;
		this.verified = verified;
	}

	static async fromDataInput(data: DataInput, id?: number) {
		return new Data(
			data.origin,
			data.translated,
			data.translator,
			data.verified,
			id,
		);
	}

	@PrimaryGeneratedColumn()
	@PrimaryColumn('int')
	id?: number;

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
