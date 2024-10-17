import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-welcome',
  templateUrl: './welcome.component.html',
  styleUrls: ['./welcome.component.scss']
})
export class WelcomeComponent implements OnInit{

  registerMode: boolean = false;
  loginMode: boolean = false;
  constructor() {}

  ngOnInit() {
  }

  loginToggle() {
    this.loginMode = true;
    if (this.registerMode === true) {
      this.registerMode = false;
    }
  }

  registerToggle() {
    this.registerMode = true;
    if (this.loginMode === true) {
      this.loginMode = false;
    }
  }

  cancelLoginMode(loginMode: boolean) {
    this.loginMode = loginMode;
  }

  cancelRegisterMode(registerMode: boolean) {
    this.registerMode = registerMode;
  }

}
