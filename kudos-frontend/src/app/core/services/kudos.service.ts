import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class KudosService {
  
  baseURL:any = '/api/kudos/';

  constructor(
    private http : HttpClient
  ) { }


  organizationList(){
    return this.http.get(`${this.baseURL}organizations/`)
  }

  signup(data:any){
    return this.http.post(`${this.baseURL}register/`, data)
  }
}
