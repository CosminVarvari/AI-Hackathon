import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/_services/auth.service';
import { ProfileComponent } from '../../profile/profile.component';
import { User } from 'src/app/_models/user';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit{
  currentUser: User | null = null;
  constructor(private router: Router, private authService: AuthService, public dialog: MatDialog) {
  }

  goToHome() {
    this.router.navigate(['home']);
  }
  
  logout() {
    localStorage.clear();
    this.router.navigate(['/welcome']);
  }

  ngOnInit(): void {
    
  }

  openDialog() {
    const user_id = this.authService.getCurrentUser().user_id;
    this.authService.getUserByID(user_id).subscribe(data => {
      this.currentUser = data;
      this.dialog.open(ProfileComponent, {
        data: this.currentUser
      });
    });
  }
}
