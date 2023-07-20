import { Module } from '@nestjs/common';
import { DataService } from './data.service';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Data } from './data.entity';
import { DataResolver } from './data.resolver';
import { UserModule } from '../user/user.module';

@Module({
	imports: [TypeOrmModule.forFeature([Data]), UserModule],
	providers: [DataService, DataResolver],
})
export class DataModule {}
