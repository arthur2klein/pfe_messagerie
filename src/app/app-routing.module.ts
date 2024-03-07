import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AccueilComponent } from './app/pages/accueil/accueil.component';
import { ConnexionComponent } from './app/pages/connexion/connexion.component';
import { DiscussionComponent } from './app/pages/discussion/discussion.component';
import { InscriptionComponent } from './app/pages/inscription/inscription.component';
import { UsersComponent } from './app/pages/users/users.component';

const routes: Routes = [
  {path:'', component:AccueilComponent },
  {path:'connexion', component:ConnexionComponent},
  {path:'inscription', component:InscriptionComponent},
  {path:'discussion', component:DiscussionComponent},
  {path:'users', component:UsersComponent}
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes),
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }