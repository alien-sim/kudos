import { HttpClient, HttpContext } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, catchError, Observable, of, switchMap, tap, throwError } from 'rxjs';
import { JWTTokenService } from './jwt-token.service';
import { LocalStorageService } from './local-storage.service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  user$ = new BehaviorSubject(null);

  constructor(
    private http: HttpClient,
    private jwtTokenService: JWTTokenService,
    private localStorageService: LocalStorageService
  ) { }

  login(data:any): Observable<any> {
    return this.http
      .post<any>(`/api/kudos/login/`, data)
      .pipe(
        tap((response) => {
          console.log(response)
          // this.user$.next(response.user);
          this.jwtTokenService.setToken(response.access);
          this.setToken("token", response.access);
          this.setToken("refreshToken", response.refresh);
        })
      );
  }

  logout(): void {  
    this.localStorageService.removeItem("token");
    this.localStorageService.removeItem("refreshToken");
  }

  private setToken(key: string, token: any): void {
    this.localStorageService.setItem(key, token);
  }

  getCurrentUser(): Observable<any> {
    return this.user$.pipe(
      switchMap((user) => {
        // check if we already have user data and force refresh is false
        if (user) {
          return of(user);
        }
        const token = this.localStorageService.getItem("token");
        // if there is token then fetch the current user
        if (token) {
          return this.fetchCurrentUser();
        }
        return of(null);
      })
    );
  }

  fetchCurrentUser(): Observable<any> {
    return this.http
      .get<any>(`/api/kudos/user-profile/`, {})
      .pipe(
        tap((user) => {
          this.user$.next(user);
        }),
        catchError((error) => {
          console.log(error);
          return throwError("fetchCurrentUser server Error");
        })
      );
  }
}
