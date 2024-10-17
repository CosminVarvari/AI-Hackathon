import { Component, Output, EventEmitter } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Credentials } from 'src/app/_models/user';
import { AuthService } from 'src/app/_services/auth.service';
import { NotificationsService } from 'src/app/_services/notifications.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
  @Output() cancelLogin = new EventEmitter();
  loginForm: FormGroup;
  hide = true;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private notifService: NotificationsService
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      const credentials: Credentials = {
        email: this.loginForm.value.email,
        password: this.loginForm.value.password,
      };
      this.authService.login(credentials).subscribe(
        (data) => {
          localStorage.setItem('token', 'Bearer ' + data[0]);
          this.router.navigate(['home']);
        },
        (error) => {
          this.notifService.error("Logging in did not work! Please try later.")
        }
      );
    }
  }

  goBack() {
    this.cancelLogin.emit(false);
  }
}
