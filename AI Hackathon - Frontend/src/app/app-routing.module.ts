import { Component, NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WelcomeComponent } from './_components/welcome/welcome.component';
import { HomeComponent } from './_components/home/home.component';
import { 
  AuthGuardService as AuthGuard 
} from './_guards/auth-guard.service';


const routes: Routes = [
  { path: 'welcome', component: WelcomeComponent},
  { path: 'home', component: HomeComponent, canActivate: [AuthGuard]},
  { path: '**', redirectTo: 'welcome', pathMatch: 'full'},
  { path: '', redirectTo: 'welcome',  pathMatch: 'full'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
