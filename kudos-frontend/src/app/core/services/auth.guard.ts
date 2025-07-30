import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { map, tap } from 'rxjs';
import { AuthService } from './auth.service';


@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate {
    constructor(
        private router: Router,
        private authService: AuthService,
    ) { }

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
        let activated = this.authService.getCurrentUser().pipe(
            map(user => {
                if (user) {
                    return true;
                }else{
                    this.router.navigateByUrl('/login');
                }
                // authorized so return true
                return !!user;
            }),
            tap(isLogged => {
                if (!isLogged) {
                    this.router.navigateByUrl('/login');
                }
            })
        );
        return activated

    }
}