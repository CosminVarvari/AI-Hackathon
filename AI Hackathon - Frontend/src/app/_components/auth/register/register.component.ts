import { Component, Output, EventEmitter } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { User } from 'src/app/_models/user';
import { AuthService } from 'src/app/_services/auth.service';
import { NotificationsService } from 'src/app/_services/notifications.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent {
  @Output() cancelRegister = new EventEmitter();
  registerForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private notifService: NotificationsService
  ) {
    this.registerForm = this.fb.group({
      firstName: ['', Validators.required],
      lastName: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      username: ['', Validators.required],
      password: ['', [Validators.required, Validators.minLength(8)]],
      confirmPassword: ['', [Validators.required, Validators.minLength(8)]]
    });
  }

  onSubmit() {
    if (this.registerForm.valid) {
      if(this.registerForm.value.password !== this.registerForm.value.confirmPassword) {
        return;
      }
      const user: User = {
        userId: null,
        first_name: this.registerForm.value.firstName,
        last_name: this.registerForm.value.lastName,
        username: this.registerForm.value.username,
        email: this.registerForm.value.email,
        password: this.registerForm.value.password,
      };
      this.authService.register(user).subscribe(
        (response) => {
          this.cancelRegister.emit(false);
          this.notifService.success("You have registered succesfully!! :)");
        },
        (error) => {
          console.error(error);
          this.notifService.error("Registration did not work! Plase try later.")
        }
      );
    }
  }

  cancel() {
    this.cancelRegister.emit(false);
  }
}