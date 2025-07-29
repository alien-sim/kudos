import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PrimeNG } from './primeNg.module';



@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    PrimeNG
  ],
  exports:[
    PrimeNG
  ]
})
export class SharedModule { }
