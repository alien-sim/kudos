import { Component } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../core/services/auth.service';
import { first } from 'rxjs';
import { MessageService } from 'primeng/api';

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss'],
    standalone: false
})
export class LoginComponent {
  form!: FormGroup;

  constructor(
    private formBuilder: FormBuilder,
    private router: Router,
    private authService: AuthService,
    private messageService: MessageService
  ){
    this.form = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email, Validators.pattern(
        /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/
      )]],
      password: ['', Validators.required]
    });
  }

  ngOnInit(){}

  onSubmit(){
    if(! this.form.valid){
      Object.keys(this.form.controls).forEach((field) => {
        const control = this.form.get(field);
        if (control instanceof FormControl) {
          control.markAsTouched({ onlySelf: true });
          control.markAsDirty({ onlySelf: true });
        }
      });
      return ;
    }
    this.authService.login(this.form.value)
    .pipe(first()).subscribe({
      next: (success:any) => {
        this.router.navigateByUrl('/dashboard');
      },
      error: (error: any) => {
        console.log("login error-- ", error);
        let detailMessage = 'Invalid email or password';
        if (error.status === 400 && error.error && error.error.non_field_errors) {
          detailMessage = error.error.non_field_errors[0];  // Get the first error message
        }
        this.messageService.add({
          severity: 'error',
          summary: 'Login Failed',
          detail: detailMessage,
          life: 3000
        });
        
      }
    });
  }
}
