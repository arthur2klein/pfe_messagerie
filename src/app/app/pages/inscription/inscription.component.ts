import { Component } from '@angular/core';
import { Injectable } from '@angular/core';
import { Router, RouterConfigurationFeature } from '@angular/router';
import { AuthService } from 'src/app/shared/services/auth.service';


@Component({
  selector: 'app-inscription',
  templateUrl: './inscription.component.html',
  styleUrls: ['./inscription.component.css']
})
export class InscriptionComponent {

}
@Injectable({
  providedIn: 'root'
})
export class UsersService {
 
  constructor(private auth: AuthService, private router:Router) { }

  //inscription: { nom: string, prenom: string, statut: string, email: string, avatar: string} = { nom: '', prenom: '', statut: '', email: '', avatar:''};
  

  
    
}

