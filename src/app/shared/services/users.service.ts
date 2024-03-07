import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { UsersI } from 'src/app/shared/models/users-i';
import { Observable } from 'rxjs';
import { Pool, QueryResult } from 'pg';  


@Injectable({
  providedIn: 'root'
})
export class UsersService {
  private pool: Pool;

  constructor(private http: HttpClient) {
    // Configuration de la connexion PostgreSQL
    this.pool = new Pool({
      user: 'votre_utilisateur',
      host: 'votre_hote',
      database: 'votre_base_de_donnees',
      password: 'votre_mot_de_passe',
      port: 5432,  // S'assurer que le port est correct
    });
  }

  getUsers(): Observable<UsersI[]> {
    const query = 'SELECT * FROM users';  // Ajouter les requêtes SQL ici

    return new Observable(observer => {
      this.pool.query(query, (error: Error, result: QueryResult) => {
        if (error) {
          observer.error(error);
        } else {
          const users: UsersI[] = result.rows;
          observer.next(users);
        }

        observer.complete();
      });
    });
  }
}
