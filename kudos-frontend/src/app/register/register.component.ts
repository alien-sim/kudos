import { Component } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../core/services/auth.service';
import { KudosService } from '../core/services/kudos.service';
import { first } from 'rxjs';
import { MessageService } from 'primeng/api';
import { MustMatch } from '../core/validators/must-match.validator';

@Component({
    selector: 'app-register',
    templateUrl: './register.component.html',
    styleUrls: ['./register.component.scss'],
    standalone: false
})
export class RegisterComponent {

  form!: FormGroup;
	orgList:any = []

  constructor(
    private formBuilder: FormBuilder,
    private messageService: MessageService,
    private kudoService: KudosService,
	private router: Router
  ){
    this.form = this.formBuilder.group({
		first_name: ['', [Validators.required, Validators.minLength(4)]],
		last_name: ['', [Validators.required, Validators.minLength(4)]],
		email: ['', [Validators.required, Validators.email, Validators.pattern(
			/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/
		)]],
		password: ['', Validators.required],
		confirm_password:['', Validators.required],
		organization: ['', Validators.required],
    },{
		validator: MustMatch('password', 'confirm_password')
	});
  }

  ngOnInit(){
		this.organizationList()
	}

	organizationList(){
		this.kudoService.organizationList()
		.pipe(first()).subscribe({
			next:(success:any) => {
				this.orgList = success
			}
		})
	}

  onSubmit(){
		if(!this.form.valid){
			Object.keys(this.form.controls).forEach((field) => {
				const control = this.form.get(field);
				if (control instanceof FormControl) {
				control.markAsTouched({ onlySelf: true });
				control.markAsDirty({ onlySelf: true });
				}
			});
			return ;
		}else{
			this.kudoService.signup(this.form.value)
			.pipe(first()).subscribe({
				next:(success:any) => {
					console.log(success)
					this.form.reset()
					this.messageService.add({
						severity: 'success',
						summary: 'Successfully Registered',
						detail: "You can login now!",
						life: 3000
					})
					// this.router.navigateByUrl('/login');
				},
				error: (error: any) => {
					console.log("login error-- ", error);
					let detailMessage = '';
					if (error.status === 400 && error.error && error.error.non_field_errors) {
					detailMessage = error.error.non_field_errors[0];  // Get the first error message
					}
					this.messageService.add({
					severity: 'error',
					summary: 'Sign Up Failed',
					detail: detailMessage,
					life: 3000
					});
					
				}
			})
		}
	}

}
