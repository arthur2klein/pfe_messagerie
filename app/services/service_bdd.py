from typing import List, Dict, Any
from dotenv import load_dotenv
import psycopg2
import os


class Service_bdd:
    def __init__(self):
        load_dotenv()

        self.conn = psycopg2.connect(
            host=os.getenv('PG_HOST'),
            database=os.getenv('PG_DATABASE'),
            user=os.getenv('PG_USER'),
            password=os.getenv('PG_PASSWORD'),
        )

    def DB_initialize(self):
        # Create a cursor
        cursor = self.conn.cursor()

        # Create a table with a POINT column
        create_table_query = """
               -- Table pour les utilisateurs
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    name VARCHAR(255),
                    email VARCHAR(255),
                    auth_id INTEGER,
                    hashed_password VARCHAR(255),
                    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                -- Table pour les groupes
                CREATE TABLE IF NOT EXISTS groups (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255),
                    owner_id INTEGER REFERENCES users(id)
                );
                
                -- Table de jonction pour les utilisateurs dans les groupes (Many-to-Many)
                CREATE TABLE IF NOT EXISTS users_in_group (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    group_id INTEGER REFERENCES groups(id),
                    CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id),
                    CONSTRAINT fk_group_id FOREIGN KEY (group_id) REFERENCES groups(id)
                );
                
                -- Table pour les messages
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    content TEXT,
                    sender_id INTEGER REFERENCES users(id),
                    receiver_group_id INTEGER REFERENCES groups(id),
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT fk_sender_id FOREIGN KEY (sender_id) REFERENCES users(id),
                    CONSTRAINT fk_receiver_group_id FOREIGN KEY (receiver_group_id) REFERENCES groups(id)
                );
                
                -- Table pour les médias
                CREATE TABLE IF NOT EXISTS medias (
                    id SERIAL PRIMARY KEY,  
                    type VARCHAR(255),
                    link VARCHAR(255),
                    message_id INTEGER REFERENCES messages(id),
                    CONSTRAINT fk_message_id FOREIGN KEY (message_id) REFERENCES messages(id)
                );

           """
        cursor.execute(create_table_query)
        self.conn.commit()

        # Close the cursor and connection
        cursor.close()

    # Définition des fonctions de service pour les opérations sur les entités de votre système

    # Opérations sur les groupes
    def rename_group(self, group_id: int, new_name: str) -> None:
        """
        Renomme un groupe avec l'identifiant `group_id` en utilisant le nouveau nom `new_name`.
        """
        pass  # Implémentation à ajouter

    def remove_user_from_group(self, group_id: int, user_id: int) -> None:
        """
        Supprime un utilisateur avec l'identifiant `user_id` du groupe avec l'identifiant `group_id`.
        """
        pass  # Implémentation à ajouter

    def add_user_to_group(self, user_id: int, group_id: int) -> None:
        """
        Ajoute un utilisateur avec l'identifiant `user_id` au groupe avec l'identifiant `group_id`.
        """
        pass  # Implémentation à ajouter

    def create_group(self) -> Dict[str, Any]:
        """
        Crée un nouveau groupe et retourne ses informations.
        """
        pass  # Implémentation à ajouter

    def get_group(self, group_id: int) -> Dict[str, Any]:
        """
        Récupère les informations d'un groupe avec l'identifiant `group_id` et les retourne.
        """
        pass  # Implémentation à ajouter

    def get_groups_user(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Récupère tous les groupes auxquels l'utilisateur avec l'identifiant `user_id` appartient et les retourne.
        """
        pass  # Implémentation à ajouter

    # Opérations sur les messages
    def create_message(self, message: Dict[str, Any]) -> int:
        """
        Crée un nouveau message avec les informations fournies et retourne son identifiant.
        """
        pass  # Implémentation à ajouter

    def create_message_with_medias(self, message: Dict[str, Any], medias: List[Dict[str, Any]]) -> int:
        """
        Crée un nouveau message avec les informations fournies et les médias associés, et retourne son identifiant.
        """
        pass  # Implémentation à ajouter

    def get_message_user_iterator(self, user_id: int):
        """
        Récupère un itérateur de messages pour l'utilisateur avec l'identifiant `user_id`.
        """
        pass  # Implémentation à ajouter

    def get_medias_message(self, message_id: int) -> List[Dict[str, Any]]:
        """
        Récupère tous les médias associés au message avec l'identifiant `message_id` et les retourne.
        """
        pass  # Implémentation à ajouter

    def get_message(self, message_id: int) -> Dict[str, Any]:
        """
        Récupère les informations d'un message avec l'identifiant `message_id` et les retourne.
        """
        pass  # Implémentation à ajouter

    def delete_message(self, message_id: int) -> None:
        """
        Supprime le message avec l'identifiant `message_id`.
        """
        pass  # Implémentation à ajouter

    # Opérations sur les médias
    def create_media(self, media: Dict[str, Any]) -> int:
        """
        Crée un nouveau média avec les informations fournies et retourne son identifiant.
        """
        pass  # Implémentation à ajouter

    def get_media(self, media_id: int) -> Dict[str, Any]:
        """
        Récupère les informations d'un média avec l'identifiant `media_id` et les retourne.
        """
        pass  # Implémentation à ajouter

    def delete_media(self, media_id: int) -> None:
        """
        Supprime le média avec l'identifiant `media_id`.
        """
        pass  # Implémentation à ajouter

    # Opérations sur les utilisateurs
    def create_user(self, user: Dict[str, Any]) -> int:
        """
        Crée un nouvel utilisateur avec les informations fournies et retourne son identifiant.
        """
        pass  # Implémentation à ajouter

    def delete_user(self, user_id: int) -> None:
        """
        Supprime l'utilisateur avec l'identifiant `user_id`.
        """
        pass  # Implémentation à ajouter

    def get_user(self, user_id: int) -> Dict[str, Any]:
        """
        Récupère les informations de l'utilisateur avec l'identifiant `user_id` et les retourne.
        """
        pass  # Implémentation à ajouter

    def get_user_auth(self, auth_id: int) -> Dict[str, Any]:
        """
        Récupère les informations de l'utilisateur avec l'identifiant d'authentification `auth_id` et les retourne.
        """
        pass  # Implémentation à ajouter

    def get_user_email(self, email: str) -> Dict[str, Any]:
        """
        Récupère les informations de l'utilisateur avec l'email `email` et les retourne.
        """
        pass  # Implémentation à ajouter

    def set_user(self, user_id: int, user: Dict[str, Any]) -> None:
        """
        Met à jour les informations de l'utilisateur avec l'identifiant `user_id` avec les informations fournies.
        """
        pass  # Implémentation à ajouter

    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Récupère toutes les informations de tous
        """
        pass

    def handle_message(self, data: Any, user_id: int) -> None:
        """
        Récupère toutes les informations de tous
        """
        pass
