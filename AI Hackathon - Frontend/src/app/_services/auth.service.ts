import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { baseUrl } from './../../environments/environment';
import { JwtHelperService } from '@auth0/angular-jwt';
import { Credentials, User } from '../_models/user';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  jwtHelper = new JwtHelperService();
  decodedToken: any;
  token: any;

  constructor(private http: HttpClient) {}

  register(user: User): Observable<User> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });
    const options = { headers };
    const body = JSON.stringify(user);
    return this.http.post<User>(baseUrl + 'api/users/register/', body, options);
  }

  login(credentials: Credentials): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });
    const options = { headers };
    const body = JSON.stringify(credentials);
    return this.http.post(baseUrl + 'api/users/login/', body, options);
  }

  logout() {
    this.token = null;
    localStorage.removeItem('token');
  }

  isAuthenticated() {
    this.token = localStorage.getItem('token');
    if (this.token === null) return false;
    if (this.token === '') return false;
    console.log(this.token);
    console.log(this.jwtHelper.isTokenExpired(this.token.toString()));
    return !this.jwtHelper.isTokenExpired(this.token.toString());
  }

  getCurrentUser() {
    if (this.isAuthenticated()) {
      this.token = localStorage.getItem('token')!.toString();
      const bearerToken = 'Bearer ' + this.token;
      this.decodedToken = this.jwtHelper.decodeToken(bearerToken);
      return this.decodedToken;
    }
    return null;
  }

  getUserByID(id: number): Observable<User> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });
    const options = { headers };
    return this.http.get<User>(`${baseUrl}api/users/user/${id}`, options);
  }
}
