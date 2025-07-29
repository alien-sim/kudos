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
	private refreshingInProgress!: boolean;
	private accessTokenSubject: BehaviorSubject<string> = new BehaviorSubject<string>(null!);

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

			// // in case of 401 http error (refresh token failed)
			// if(err instanceof HttpErrorResponse && err.status === 401 && err.url?.includes('refresh_token')){
			//   // otherwise logout and redirect to login page
			//   return this.logoutAndRedirect(err);
			// }
			// in case of 401 http error
			if (err instanceof HttpErrorResponse && err.status === 401) {
				// get refresh tokens
				const refreshToken = this.localStorageService.getItem('refreshToken');

				// if there are tokens then send refresh token request
				if (refreshToken && accessToken) {
					return this.refreshToken(req, next);
				}

				// otherwise logout and redirect to login page
				return this.logoutAndRedirect(err);
			}

			// // in case of 403 http error (refresh token failed)
			if (err instanceof HttpErrorResponse && err.status === 403) {
				// return this.refreshToken(req, next);
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
		this.router.navigate(['/account/login'], {
			replaceUrl: true,
			state: {}, // or omit it entirely
		});
		// this.router.navigateByUrl('/account/login');

		return throwError(err);
	}

	private refreshToken(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
		if (!this.refreshingInProgress) {
			this.refreshingInProgress = true;
			this.accessTokenSubject.next(null!);

			return this.authService.refreshToken().pipe(
				switchMap((res) => {
					console.log('refresh response intercept -', res)
					this.refreshingInProgress = false;
					this.accessTokenSubject.next(res.access);
					// repeat failed request with new token
					return next.handle(this.addAuthorizationHeader(request, res.access));
				}),
				catchError((err) => {
					// repeat failed request with new token
					return this.logoutAndRedirect(err);
				})
			);
		} else {
			// wait while getting new token
			return this.accessTokenSubject.pipe(
				filter(token => token !== null),
				take(1),
				switchMap(token => {
					// repeat failed request with new token
					return next.handle(this.addAuthorizationHeader(request, token));
				}
			));
		}
	}
}
