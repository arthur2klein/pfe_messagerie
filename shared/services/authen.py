import psycopg2
import os
import bcrypt
from uuid import uuid4

class AuthService:
    def __init__(self):
        pass

    def connect_db(self):
        """Établit une connexion à la base de données."""
        return psycopg2.connect(
                dbname = os.getenv("AUTH_DATABASE", 'pfe_database_auth'),
                user = os.getenv("AUTH_USER", 'my_user'),
                password = os.getenv("AUTH_PASSWORD", 'my_password'),
                host = os.getenv("AUTH_HOST", 'auth_db'),
                port = int(os.getenv("AUTH_PORT", '5432')),
                )

    def create_account(self, email: str, password: str):
        """Crée un nouveau compte utilisateur avec un email et un mot de passe.
        """
        with self.connect_db() as conn:
            with conn.cursor() as cur:
                try:
                    # Hash le mot de passe et convertit l'UUID en chaîne
                    hashed_password = bcrypt.hashpw(
                            password.encode('utf-8'),
                            bcrypt.gensalt()
                            )
                    auth_id = str(uuid4())
                    # Insère le nouvel utilisateur dans la base de données
                    cur.execute(
                            "INSERT INTO MyUser "
                            "(auth_id, email, password) VALUES (%s, %s, %s)",
                            (auth_id, email, hashed_password)
                            )
                    conn.commit()
                    return True, auth_id
                except psycopg2.IntegrityError:
                    conn.rollback()
                    return False, "An account with this email already exists."
                except Exception as e:
                    conn.rollback()
                    return False, f"Failed to create account: {e}"

    def change_account(
            self,
            email: str,
            new_email: str = None,
            new_password: str = None
            ):
        """Modifie l'email ou le mot de passe d'un compte utilisateur existant.
        """
        with self.connect_db() as conn:
            with conn.cursor() as cur:
                try:
                    if new_password:
                        hashed_password = bcrypt.hashpw(
                                new_password.encode('utf-8'),
                                bcrypt.gensalt()
                                )
                        cur.execute(
                                "UPDATE MyUser "
                                "SET password = %s WHERE email = %s",
                                (hashed_password, email)
                                )
                    if new_email:
                        cur.execute(
                                "UPDATE MyUser "
                                "SET email = %s WHERE email = %s",
                                (new_email, email)
                                )
                    conn.commit()
                    return True, "Account updated successfully."
                except Exception as e:
                    conn.rollback()
                    return False, f"Failed to update account: {e}"

    def login(self, email: str, password: str):
        """Vérifie les identifiants d'un utilisateur et permet la connexion.
        """
        with self.connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                        "SELECT password, auth_id FROM MyUser WHERE email = %s",
                        (email,)
                        )
                user_record = cur.fetchone()
                if user_record:
                    if user_record[0].startswith('\\x'):
                        hashed_password = bytes.fromhex(user_record[0][2:])
                    else:
                        hashed_password = user_record[0].encode('utf-8')

                    if bcrypt.checkpw(
                            password.encode('utf-8'),
                            hashed_password
                            ):
                        return True, user_record[1]
                    else:
                        return False, "Invalid email or password."
                else:
                    return False, "Invalid email or password."

    def delete_account(self, email: str):
        """Supprime un compte utilisateur de la base de données.
        """
        with self.connect_db() as conn:
            with conn.cursor() as cur:
                try:
                    # Exécute la commande de suppression
                    cur.execute(
                            "DELETE FROM MyUser WHERE email = %s",
                            (email,)
                            )
                    if cur.rowcount == 0:
                        # Aucune ligne affectée signifie que l'utilisateur
                        # n'existait pas
                        return False, "No account found with the specified email."
                    else:
                        conn.commit()
                        return True, "Account deleted successfully."
                except Exception as e:
                    conn.rollback()
                    return False, f"Failed to delete account: {e}"
