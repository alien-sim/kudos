import { Component } from '@angular/core';
import { AuthService } from '../core/services/auth.service';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
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
    receivedKudoList:any = []
    sendKudoForm !: FormGroup
    userList:any = []
    showMsg:any = false
    kudoDetail:any 

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
        this.receivedKudos()
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

    receivedKudos(){
        this.kudoService.receivedKudo()
        .pipe(first()).subscribe({
            next:(success:any) => {
                this.receivedKudoList = success;
            }
        })
    }

    sendKudo(){
        if(!this.sendKudoForm.valid){
            Object.keys(this.sendKudoForm.controls).forEach((field) => {
                const control = this.sendKudoForm.get(field);
                if (control instanceof FormControl) {
                control.markAsTouched({ onlySelf: true });
                control.markAsDirty({ onlySelf: true });
                }
            });
            return ;
        }
        console.log(this.sendKudoForm.value)
        this.kudoService.sendKudo(this.sendKudoForm.value)
        .pipe(first()).subscribe({
            next:(success:any) => {
                this.sendKudoForm.reset()
                this.messageService.add({
                    severity:'success',
                    summary:"Kudo Successfully sent",
                    life: 3000
                })
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

    showKudoMsg(kudo:any){
        this.showMsg = true
        this.kudoDetail = kudo
    }

}
