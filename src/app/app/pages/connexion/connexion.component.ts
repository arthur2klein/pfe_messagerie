import { Component } from '@angular/core';
import { AuthService } from 'src/app/shared/services/auth.service';




@Component({
  selector: 'app-connexion',
  templateUrl: './connexion.component.html',
  styleUrls: ['./connexion.component.css']
})
export class ConnexionComponent {

  ngOnInit() {
   console.log('test');
  }
  constructor(public auth:AuthService){}

  
}

