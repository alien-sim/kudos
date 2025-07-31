import { Component } from '@angular/core';
import { AuthService } from '../core/services/auth.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { KudosService } from '../core/services/kudos.service';
import { first } from 'rxjs';
import { MessageService } from 'primeng/api';
import { Router } from '@angular/router';

@Component({
    selector: 'app-dashboard',
    templateUrl: './dashboard.component.html',
    styleUrls: ['./dashboard.component.scss'],
    standalone: false
})
export class DashboardComponent {

    user:any = {}
    sendKudoForm !: FormGroup
    userList:any = []

    constructor(
        private authService: AuthService,
        private formBuilder: FormBuilder,
        private kudoService: KudosService,
        private messageService: MessageService,
        private router: Router
    ){
        this.sendKudoForm = this.formBuilder.group({
            reciever : ['', Validators.required],
            message : ['', Validators.required]
        })
    }

    ngOnInit(){
        this.authService.user$.subscribe((data) => {
            this.user = data
        })
        this.getUserList()
    }

    logout(){
        this.authService.logout()
        this.router.navigate(['/login'], {
			replaceUrl: true,
			state: {}, // or omit it entirely
		});
    }

    getUserList(){
        this.kudoService.getOrgUsers()
        .pipe(first()).subscribe({
            next:(success:any) => {
                console.log(success)
                this.userList = success
            }
        })
    }

    sendKudo(){
        if(!this.sendKudoForm.valid){
            return
        }
        console.log(this.sendKudoForm.value)
        this.kudoService.sendKudo(this.sendKudoForm.value)
        .pipe(first()).subscribe({
            next:(success:any) => {
                console.log(success)
                this.sendKudoForm.reset()
            },
            error:(error:any) => {
                // console.log(error.error.reciever)
                this.messageService.add({
                    severity:'error',
                    summary:error.error.reciever[0],
                    life: 3000
                })
            }
        })
    }

}
