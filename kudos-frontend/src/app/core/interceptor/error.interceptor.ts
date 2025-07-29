import { HttpEvent, HttpHandler, HttpRequest, HttpErrorResponse, HttpInterceptor, HttpContextToken } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Router } from "@angular/router";

import { Observable, throwError } from "rxjs";
import { catchError, retry } from "rxjs/operators";
import { AuthService } from "../services/auth.service";
// import { ToastrService } from 'ngx-toastr';

export const SHOW_DIALOG = new HttpContextToken(() => true);

@Injectable()
export class ErrorIntercept implements HttpInterceptor {
  constructor(
    // private toastr: ToastrService
    private authService: AuthService,
    private router: Router
  ) { }

  intercept(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(
      // retry(1),
      catchError((error: HttpErrorResponse) => {
        let errorMessage = "";
        const showDialog = request.context.get(SHOW_DIALOG);
        console.log("error interceptor n", showDialog);

        if (error.error instanceof ErrorEvent) {
          // client-side error
          errorMessage = `Error: ${error.error.message}`;
        } else {
          // server-side error
          let message = ''
          if (error.status === 403) {
            console.log("403 error interceptor")
            this.authService.logout();
            this.router.navigate(['/login'], {
              replaceUrl: true,
              state: {}, // or omit it entirely
            });
          } 
          else {
            if (error?.error?.errors?.length > 0) {
              message = error?.error?.errors[0]?.detail
            } else if (error?.error?.non_field_errors?.length) {
              message = error?.error?.non_field_errors[0]
            } else {
              message = error.error.message
            }
            // message = error?.error?.errors?.length >0 ? error?.error?.errors[0]?.detail : error.error.message;
            errorMessage = `Error Status: ${error.status}\nMessage: ${message}`;
            console.log(errorMessage);
          }
        }
        return throwError(error);
      })
    );
  }
}
