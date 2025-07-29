import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LocalStorageService {

  constructor() { }
  private storageSub= new Subject<string>();

  watchStorage(): Observable<any> {
    return this.storageSub.asObservable();
  }

  setItem(key: string, value: any): void {
    localStorage.setItem(key, JSON.stringify(value));
    this.storageSub.next(key);
  }

  getItem(key: string): any {
    try {
      const item = localStorage.getItem(key);

      return JSON.parse(item!);
    } catch (e) {
      return null;
    }
  }

  removeItem(key: string): any {
    localStorage.removeItem(key);
    this.storageSub.next("removed");
  }

  clear(): void {
    localStorage.clear();
  }
}
