import { Module } from '@nestjs/common';
import { DataService } from './data.service';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Data } from './data.entity';
import { DataResolver } from './data.resolver';
import { UserService } from 'src/user/user.service';
import { User } from 'src/user/user.entity';
import { Session } from 'src/user/session.entity';

@Module({
	providers: [DataService, DataResolver, UserService],
	imports: [TypeOrmModule.forFeature([Data, User, Session])],
})
export class DataModule {}
