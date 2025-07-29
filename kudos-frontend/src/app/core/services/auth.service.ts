import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, tap } from 'rxjs';
import { JWTTokenService } from './jwt-token.service';
import { LocalStorageService } from './local-storage.service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

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
}
