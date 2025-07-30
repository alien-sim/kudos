import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HttpErrorResponse, HttpContextToken } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { catchError, filter, switchMap, take } from 'rxjs/operators';

import { LocalStorageService } from '../services/local-storage.service';
import { AuthService } from '../services/auth.service';

export const NO_TOKEN = new HttpContextToken(() => false);

@Injectable()
export class TokenInterceptor implements HttpInterceptor {

	constructor(
		private localStorageService: LocalStorageService,
		private authService: AuthService,
		private router: Router
	) {}

	intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
		const noToken = req.context.get(NO_TOKEN);
		// console.log('token interceptor no-token',noToken)
		// If no token found then redirect to login
		if(noToken){
			console.log('No token added in req')
			return this.logoutAndRedirect(req);
			// return next.handle(req);
		}
		const accessToken = this.localStorageService.getItem('token');

		return next.handle(this.addAuthorizationHeader(req, accessToken)).pipe(
		catchError(err => {

			if (err instanceof HttpErrorResponse && err.status === 401) {
				// get refresh tokens
				const refreshToken = this.localStorageService.getItem('refreshToken');

				// if there are tokens then send refresh token request
				// if (refreshToken && accessToken) {
				// 	return this.refreshToken(req, next);
				// }

				// otherwise logout and redirect to login page
				return this.logoutAndRedirect(err);
			}

			// // in case of 403 http error (refresh token failed)
			if (err instanceof HttpErrorResponse && err.status === 403) {
				// logout and redirect to login page
				return this.logoutAndRedirect(err);
			}
			// if error has status neither 401 nor 403 then just return this error
			return throwError(err);
		})
		);
	}

	private addAuthorizationHeader(request: HttpRequest<any>, token: string): HttpRequest<any> {
		if (token) {
		return request.clone({setHeaders: {Authorization: `Bearer ${token}`}});
		}

		return request;
	}

	private logoutAndRedirect(err:any): Observable<HttpEvent<any>> {
		this.authService.logout();
		this.router.navigate(['/login'], {
			replaceUrl: true,
			state: {}, // or omit it entirely
		});

		return throwError(err);
	}

	
}
