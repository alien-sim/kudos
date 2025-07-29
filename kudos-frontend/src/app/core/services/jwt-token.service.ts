import { Injectable } from '@angular/core';
import { jwtDecode } from "jwt-decode";


@Injectable({
  providedIn: 'root'
})
export class JWTTokenService {

    jwtToken!: string;
    decodedToken!: { [key: string]: string; };

    constructor() {
    }

    setToken(token: string) {
      if (token) {
        this.jwtToken = token;
      }
    }

    private decodeToken() {
      if (this.jwtToken) {
      this.decodedToken = jwtDecode(this.jwtToken); 
      }
    }

    getDecodeToken() {
      return jwtDecode(this.jwtToken);
    }

    getUser() {
      this.decodeToken();
      return this.decodedToken ? this.decodedToken['displayname'] : null;
    }

}