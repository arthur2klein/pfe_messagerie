from __future__ import annotations
from typing import Type
from shared.models.message import Message
from shared.models.group import Group
from shared.exceptions.database_exception import DatabaseException
import psycopg2
from psycopg2 import sql

class Service_bdd:
    """ Gives access to the database for the rest of the program.
    ---
    Attributes:
        connection (psycopg2.extensions.connection): Connection to the database.
        cursor (psycopg2.extensions.cursor): Cursor in the database.
    ---
    Methods:
    """

    def __init__(self: Self):
        """ Creates a new database access service.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        ```
        """
        try:
            self.connection = psycopg2.connect(
                    dbname = 'pfe_database',
                    user = 'my_user',
                    password = 'my_password',
                    host = 'postgres',
                    port = 5432,
                    )
            self.cursor = self.connection.cursor()
        except Exception as e:
            raise DatabaseException(f'Failed to instanciate the database service: {e}')

    def fetch_query(
            self: Self,
            query: str,
            params: list[Any]=None
            ) -> list[tuple[Any]]:
        """ Executes the given query on the database to fetch data.
        ---
        Parameters:
            query (str): Query to execute, parameters use %s placeholders.
            params (list[Any]): Parameters of the query.
        ---
        Returns:
            (list[typle[Any]]): List of the rows returned by the database for
            the given query.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        service_bdd.fetch_query(
                "SELECT * FROM Table WHERE name = %s",
                ["name"]
                )
        ```
        """
        try:
            self.cursor.execute(sql.SQL(query), params)
            res = self.cursor.fetchall()
        except Exception as e:
            raise DatabaseException(f'Failed to execute query {query}: {e}')
        return res

    def change_query(
            self: Self,
            query: str,
            params: list[Any]=None
            ) -> list[tuple[Any]]:
        """ Executes the given query on the database to change data.
        ---
        Parameters:
            query (str): Query to execute, parameters use %s placeholders.
            params (list[Any]): Parameters of the query.
        ---
        Returns:
            (list[typle[Any]]): List of the rows returned by the database for
            the given query.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        service_bdd.change(
                "SELECT * FROM Table WHERE name = %s",
                ["name"]
                )
        ```
        """
        try:
            self.cursor.execute(sql.SQL(query), params)
            res = self.cursor.fetchall()
            self.connection.commit()
        except Exception as e:
            raise DatabaseException(f'Failed to execute query {query}: {e}')
        return res

    def close_connection(self):
        """ Close the connection to the database.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        service_bdd.close_connection()
        ```
        """
        self.cursor.close()
        self.connection.close()

    def __del__(self: Self):
        """ Deletes the current instance.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Example:
        ```python
        my_service = Service_bdd()
        del my_service
        ```
        """
        self.close_connection()

    def iter_message_first(self: Self, group_id: str) -> Message:
        """ Returns the first message to load for a given group.
        ---
        Parameters:
            self (Self): Current instance.
            group_id (str): Id of the group to load the message of.
        ---
        Returns:
            (Message): First message to load.
        ---
        Raises:
            (DatabaseException): If the query fails.
            (StopIteration): If no message if found.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        message = service_bdd.iter_message_first('3')
        ```
        """
        return self.oldest_message(group_id)

    def oldest_message(self: Self, group_id: str) -> Message:
        """ Returns the oldest message to load for a given group.
        ---
        Parameters:
            self (Self): Current instance.
            group_id (str): Id of the group to load the message of.
        ---
        Returns:
            (Message): Oldest message of the group.
        ---
        Raises:
            (DatabaseException): If the query fails.
            (StopIteration): If no message if found.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        message = service_bdd.oldest_message('3')
        ```
        """
        try:
            query_result = self.fetch_query(
                    "SELECT * FROM message "
                    "WHERE receiver_group_id = %s "
                    "ORDER BY date ASC Limit 1",
                    [group_id]
                    )
        except Exception as e:
            raise DatabaseException(
                    f'Could not execute the query to get the oldest message '
                    f'for {group_id=}: {e}'
                    )
        try:
            res = query_result[0]
        except IndexError:
            raise StopIteration('No message found for the given group.')
        return Message(*res[1:], id = res[0])

    def iter_message_next(self: Self, current: Message) -> Message:
        """ Returns the message which should be loaded after the given message.
        ---
        Parameters:
            self (Self): Current instance.
            current (Message): Message previously loaded.
        ---
        Returns:
            (Message): Next message to load.
        ---
        Raises:
            (DatabaseException): If the query fails.
            (StopIteration): If no message if found.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        message = service_bdd.iter_message_first('3')
        next_message = service_bdd.iter_message_next(message)
        ```
        """
        group_id = current.receiver_group_id
        date = current.date
        try:
            query_result = self.fetch_query(
                    "SELECT * FROM message "
                    "WHERE receiver_group_id = %s "
                    "AND date > %s "
                    "ORDER BY date ASC Limit 1",
                    [group_id, date]
                    )
        except Exception as e:
            raise DatabaseException(
                    f'Could not execute the query to get the next message '
                    f'for {group_id=}: {e}'
                    )
        try:
            res = query_result[0]
        except IndexError:
            raise StopIteration('No next message found for the given group.')
        return Message(*res[1:], id = res[0])

    def rename_group(
            self: Self,
            group_id: str,
            new_name: str
            ):
        """ Rename the given group.
        ---
        Parameters:
            self (Self): Current instance.
            group_id (str): Id of the group to rename.
            new_name (str): New name for the group.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        service_bdd.rename_group('4', 'new_name')
        ```
        """
        query = "UPDATE groups SET name = %s WHERE id = %s"
        try:
            self.change_query(query, [new_name, group_id])
        except Exception as e:
            raise DatabaseException(
                    f'Failed to rename the group {group_id}: {e}'
                    )

    def remove_user_from_group(
            self: Self,
            user_id: str
            group_id: str,
            ):
        """ Remove the given user from the given group.
        ---
        Parameters:
            self (Self): Current instance.
            user_id (str): Id of the user to remove from the group.
            group_id (str): Id of the group to remove the user from.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        service_bdd.remove_user_from_group('user_id', 'group_id')
        ```
        """
        query = 'DELETE FROM useringroup WHERE group_id = %s AND user_id = %s'
        try:
            self.change_query(query, [user_id, group_id])
        except Exception as e:
            raise DatabaseException(
                    f'Failed to remove the user {user_id} from the group '
                    f'{group_id}: {e}'
                    )

    def add_user_to_group(
            self: Self,
            user_id: str,
            group_id: str
            ):
        """ Adds the given user to the given group.
        ---
        Parameters:
            self (Self): Current instance.
            user_id (str): User to add to the group.
            group_id (str): Group to add the user to.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        service_bdd.remove_user_from_group('user_id', 'group_id')
        ```
        """
        query = 'INSERT INTO useringroup (user_id, group_id) VALUES (%s, %s)'
        try:
            self.change_query(query, [user_id, group_id])
        except Exception as e:
            raise DatabaseException(
                    f'Failed to add the user {user_id} to the group '
                    f'{group_id}: {e}'
                    )

    def create_group(self: Self, group: Group) -> str:
        """ Creates the given group in the database.
        Does not add the user in the group in the database.
        ---
        Parameters:
            self (Self): Current instance.
            group (Group): Group to create (will receive its id).
        ---
        Returns:
            (str): Id of the group in the database.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        my_group = Group('my_group')
        my_group_id = my_service.create_group(my_group)
        ```
        """
        query = 'INSERT INTO groups (name) VALUES (%s) RETURNING id'
        try:
            group_id = self.change_query(query, [group.name])[0][0]
            group.set_id(group_id)
        except Exception as e:
            raise DatabaseException(
                    f'Failed to create the group {group}: {e}'
                    )
        return group_id

    def get_group(self: Self, group_id: str) -> Group:
        """ Returns the group with the given id.
        ---
        Parameteres:
            self (Self): Current instance.
            group_id (str): Id of the group to get.
        ---
        Returns:
            (Group): Group with the given id.
        ---
        Raises:
            (DatabaseException): If the querry fails.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        my_group = Group('my_group')
        my_group_id = my_service.create_group(my_group)
        assert(my_group == service_bdd.get_group(my_group_id))
        ```
        """
        query = 'SELECT * FROM groups WHERE id = %s'
        try:
            group = self.fetch_query(query, [group_id])[0]
        except Exception as e:
            raise DatabaseException(f'Could not get the group {group_id}: {e}')
        return Group(*group[1:], id = group[0])

    def get_groups_user(self: Self, user_id: str) -> list[Group]:
        """ Returns all the group of a given user.
        ---
        Parameters:
            self (Self): Current instance.
            user_id (str): Id of the user to get the groups of.
        ---
        Returns:
            (list[Group]): Groups of the given user.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        groups = service_bdd.get_groups_user('user_id')
        ```
        """
        query = ('SELECT groups.* FROM groups '
                 'JOIN useringroup ON groups.id = useringroup.group_id '
                 'WHERE useringroup.user_id = %s')
        try:
            groups = self.fetch_query(query, [user_id])
        except Exception as e:
            raise DatabaseException(
                    f'Could not get the groups of user {user_id}: {e}'
                    )
        return [Group(*line[1:], id = line[0]) for line in groups]

    def create_message(self: Self, message: Message) -> str:
        """ Create a new message in the database.
        ---
        Parameters:
            self (Self): Current instance.
            message (Message): Message to add to the database, will receive its
            id.
        ---
        Returns:
            (str): Id of the message.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        my_message = Message(
                'content',
                'sender_id',
                'receiver_id',
                'receiver_group_id',
                0
                )
        service_bdd = Service_bdd()
        message_id = service_bdd.create_message(my_message)
        ```
        """
        query = ('INSERT INTO messages '
                 '(content, sender_id, receiver_group_id, date_) '
                 'VALUES (%s, %s, %s) RETURNING id')
        try:
            message_id = self.change_query(
                    query,
                    [message.content,
                     message.sender_id,
                     message.receiver_group_id,
                     message.date
                     ]
                    )
            message.set_id(message_id)
        except Exception as e:
            raise DatabaseException(
                    f'Could not create the message {message}: {e}'
                    )
        return message_id

            """ TODO
    create_message_with_medias(message, list[medias]),
    get_message_user_iterator(user_id) -> message_iterator,
    get_medias_message(message_id) -> list[medias],
    get_message(message_id),
    delete_message(message_id),
    create_media(media) -> media_id,
    get_media(media_id) -> media,
    delete_media(media_id),
    create_message(message) -> message_id,
    create_user(user) -> user_id,
    delete_user(user_id),
    get_user(user_id),
    get_user_auth(auth_id) -> user,
    get_user_email(email) -> user,
    set_user(user_id, user),
    get_all_users() -> list[user].
    """
