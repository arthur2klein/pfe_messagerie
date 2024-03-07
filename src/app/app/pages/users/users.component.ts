import { Component, OnInit } from '@angular/core';
import { UsersI } from 'src/app/shared/models/users-i';
import { UsersService } from 'src/app/shared/services/users.service';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.css']
})
export class UsersComponent implements OnInit {
  
  listeUsers: UsersI[] = [];
  filtre: string = '';
  //users :any;
  users: UsersI[] = [];
  
  constructor(private usersService: UsersService) { }
  
  ngOnInit(): void {
    this.usersService.getUsers().subscribe(users => {
      this.users = users;
    });
  }
  
  filtrerUtilisateurs() {
    if (!this.filtre) {
      return this.listeUsers;
    }
    
    return this.listeUsers.filter((user: UsersI) =>
      user.name.toLowerCase().includes(this.filtre.toLowerCase()) ||
      user.first_name.toLowerCase().includes(this.filtre.toLowerCase()) ||
      user.email.toLowerCase().includes(this.filtre.toLowerCase())
    );
  }
}
