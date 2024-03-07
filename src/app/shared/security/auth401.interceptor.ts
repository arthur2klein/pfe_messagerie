import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpHeaders,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';

@Injectable()
export class Auth401Interceptor implements HttpInterceptor {
  entetes:any;  
constructor (private user: AuthService, private router:Router){}
  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
//If i'm connected and i have a token inside my profile
    return next.handle(request).pipe(
      erreur =>{
        if (erreur instanceof HttpErrorResponse && erreur.status == 401){
          this.user.isLoggedIn = false;
          this.router.navigateByUrl('/connexion');
        }

        return erreur;
      }
    )
}


}