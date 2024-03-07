import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FooterComponent } from './Template/footer/footer.component';
import { MenuComponent } from './Template/menu/menu.component';
import { AccueilComponent } from './app/pages/accueil/accueil.component';
import { ConnexionComponent } from './app/pages/connexion/connexion.component';
import { DiscussionComponent } from './app/pages/discussion/discussion.component';
import { UsersComponent } from './app/pages/users/users.component';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { InscriptionComponent } from './app/pages/inscription/inscription.component';

@NgModule({
  declarations: [
    AppComponent,
    FooterComponent,
    MenuComponent,
    AccueilComponent,
    ConnexionComponent,
    AppComponent,
    DiscussionComponent,
    UsersComponent,
    InscriptionComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    RouterModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule { }
