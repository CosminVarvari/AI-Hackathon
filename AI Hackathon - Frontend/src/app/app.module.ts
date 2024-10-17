import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
//Modules
import { MaterialModule } from './material/material.module';
//Providers
import { AuthInterceptor } from './interceptors/auth.interceptor';
//Components
import { HomeComponent } from './_components/home/home.component';
import { NavbarComponent } from './_components/shared/navbar/navbar.component';
import { WelcomeComponent } from './_components/welcome/welcome.component';
import { LoginComponent } from './_components/auth/login/login.component';
import { RegisterComponent } from './_components/auth/register/register.component';
import { FooterComponent } from './_components/shared/footer/footer.component';
import { ProfileComponent } from './_components/profile/profile.component';
import { FilterPipe } from './_components/shared/filter.pipe';

@NgModule({
  declarations: [
    AppComponent,
    WelcomeComponent,
    LoginComponent,
    RegisterComponent,
    HomeComponent,
    NavbarComponent,
    FooterComponent,
    ProfileComponent,
    FilterPipe
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    FormsModule,
    MaterialModule
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
