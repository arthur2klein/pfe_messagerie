import psycopg2
import bcrypt
from uuid import uuid4

class AuthService:
    def __init__(self, dsn):
        self.dsn = dsn

    def connect_db(self):
        """Établit une connexion à la base de données."""
        return psycopg2.connect(self.dsn)

    def create_account(self, email: str, password: str):
        """Crée un nouveau compte utilisateur avec un email et un mot de passe."""
        with self.connect_db() as conn:
            with conn.cursor() as cur:
                try:
                    # Hash le mot de passe et convertit l'UUID en chaîne
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    auth_id = str(uuid4())
                    # Insère le nouvel utilisateur dans la base de données
                    cur.execute("INSERT INTO users (email, password, auth_id) VALUES (%s, %s, %s)", 
                                (email, hashed_password, auth_id))
                    conn.commit()
                    return "Account created successfully."
                except psycopg2.IntegrityError:
                    conn.rollback()
                    return "An account with this email already exists."
                except Exception as e:
                    conn.rollback()
                    return f"Failed to create account: {e}"

    def change_account(self, email: str, new_email: str = None, new_password: str = None):
        """Modifie l'email ou le mot de passe d'un compte utilisateur existant."""
        with self.connect_db() as conn:
            with conn.cursor() as cur:
                try:
                    if new_password:
                        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                        cur.execute("UPDATE users SET password = %s WHERE email = %s", 
                                    (hashed_password, email))
                    if new_email:
                        cur.execute("UPDATE users SET email = %s WHERE email = %s", 
                                    (new_email, email))
                    conn.commit()
                    return "Account updated successfully."
                except Exception as e:
                    conn.rollback()
                    return f"Failed to update account: {e}"

    def login(self, email: str, password: str):
        """Vérifie les identifiants d'un utilisateur et permet la connexion."""
        with self.connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT password FROM users WHERE email = %s", (email,))
                user_record = cur.fetchone()
                if user_record:
                    if user_record[0].startswith('\\x'):
                        hashed_password = bytes.fromhex(user_record[0][2:])
                    else:
                        hashed_password = user_record[0].encode('utf-8')
                    
                    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                        return "Login successful."
                    else:
                        return "Invalid email or password."
                else:
                    return "Invalid email or password."
    
    def delete_account(self, email: str):
        """Supprime un compte utilisateur de la base de données."""
        with self.connect_db() as conn:
            with conn.cursor() as cur:
                try:
                    # Exécute la commande de suppression
                    cur.execute("DELETE FROM users WHERE email = %s", (email,))
                    if cur.rowcount == 0:
                        # Aucune ligne affectée signifie que l'utilisateur n'existait pas
                        return "No account found with the specified email."
                    else:
                        conn.commit()
                        return "Account deleted successfully."
                except Exception as e:
                    conn.rollback()
                    return f"Failed to delete account: {e}"

# Example usage
if __name__ == "__main__":
    dsn = "dbname='pfe_database' user='my_user' host='localhost' password='my_password' port='5433'"
    auth_service = AuthService(dsn)

    # Create an account
    print(auth_service.create_account("test@example.com", "newSecurePassword123"))

    # Attempt to login
    print(auth_service.login("test@example.com", "newSecurePassword123"))

    # Change the account details
    print(auth_service.change_account("test@example.com", new_password="newSecurePassword123"))

    # Delete the account
    print(auth_service.delete_account("test@example.com"))

