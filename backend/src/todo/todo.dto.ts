import { Field, InputType, ObjectType } from '@nestjs/graphql';
import { Entity } from 'typeorm';

@Entity()
@InputType('TodoInput')
@ObjectType('TodoOutput')
export class TodoObj {
	constructor(
		jobDescription: string = '',
		deadline: Date = new Date('1890-05-19'),
		finished: boolean = false,
	) {
		this.jobDescription = jobDescription;
		this.deadline = deadline;
		this.finished = finished;
	}

	@Field(() => String, { nullable: true })
	id?: string;

	@Field(() => String)
	jobDescription: string;

	@Field(() => Date)
	deadline: Date;

	@Field(() => Boolean)
	finished: boolean;
}
