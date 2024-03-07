import { Component } from '@angular/core';
import { UsersI } from 'src/app/shared/models/users-i';
import { NgModel } from '@angular/forms';

@Component({
  selector: 'app-discussion',
  templateUrl: './discussion.component.html',
  styleUrls: ['./discussion.component.css']
})
export class DiscussionComponent {
  listeUsers: UsersI[] = [];
  filtre: string = '';
  ngOnInit() {
    // Chargez la liste des utilisateurs au moment de l'initialisation du composant
    this.listeUsers;
  }
  filtrerUtilisateurs() {
    if (!this.filtre) {
      // Si le filtre est vide, afficher tous les utilisateurs
      return this.listeUsers;
    }

    // Utiliser la méthode filter pour filtrer les utilisateurs par nom, prénom ou email
    return this.listeUsers.filter((user: { name: string; first_name: string; email: string; }) =>
      user.name.toLowerCase().includes(this.filtre.toLowerCase()) ||
      user.first_name.toLowerCase().includes(this.filtre.toLowerCase()) ||
      user.email.toLowerCase().includes(this.filtre.toLowerCase())
    );
  }
}
