import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../core/services/auth.service';
import { KudosService } from '../core/services/kudos.service';
import { first } from 'rxjs';
import { MessageService } from 'primeng/api';

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
			first_name: ['', Validators.required],
			last_name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
			confirm_password:['', Validators.required],
			organization: ['', Validators.required],
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
				}
			})
		}
	}

}
