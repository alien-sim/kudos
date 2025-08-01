import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { LoginRoutingModule } from './login-routing.module';
import { LoginComponent } from './login.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from '../shared/shared.module';
import { MessageService } from 'primeng/api';


@NgModule({
  declarations: [
    LoginComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    SharedModule,
    ReactiveFormsModule,
    LoginRoutingModule
  ],
  providers:[
    MessageService
  ]
})
export class LoginModule { }
