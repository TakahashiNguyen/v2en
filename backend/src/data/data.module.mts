import { Module } from '@nestjs/common';
import { DataService } from './data.service.mjs';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Data } from './data.entity.mjs';
import { DataResolver } from './data.resolver.mjs';
import { UserModule } from '../user/user.module.mjs';

@Module({
	imports: [TypeOrmModule.forFeature([Data]), UserModule],
	providers: [DataService, DataResolver],
})
export class DataModule {}
