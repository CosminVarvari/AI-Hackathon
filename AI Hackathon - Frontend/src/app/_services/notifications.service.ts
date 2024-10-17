import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

@Injectable({
  providedIn: 'root',
})
export class NotificationsService {
  constructor(private _snackBar: MatSnackBar) {}

  success(message: string) {
    this._snackBar.open('Success! ' + message, 'Cancel', {
      duration: 5000,
      horizontalPosition: 'right',
      verticalPosition: 'bottom',
    });
  }

  error(message: string) {
    this._snackBar.open('Error! ' + message, 'Cancel', {
      duration: 5000,
      horizontalPosition: 'right',
      verticalPosition: 'bottom',
    });
  }

  warning(message: string) {
    this._snackBar.open('Warning! ' + message, 'Cancel', {
      duration: 5000,
      horizontalPosition: 'right',
      verticalPosition: 'bottom',
    });
  }
}
