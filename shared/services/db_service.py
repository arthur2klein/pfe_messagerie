from __future__ import annotations
from typing import Type
from shared.models.message import Message
from shared.models.media import Media
from shared.models.group import Group
from shared.models.user import User
from shared.services.message_iterator import Message_iterator
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
        - __init__(Self): Creates a new database access service.
        - fetch_query(Self,str,list[Any]=None) -> list[tuple[Any]]: Executes
          the given query on the database to fetch data.
        - change_query(Self,str,list[Any]=None) -> list[tuple[Any]]: Executes
          the given query on the database to change data.
        - close_connection(self): Close the connection to the database.
        - __del__(Self): Deletes the current instance.
        - get_all_messages_group(Self,str) ->
          list[Message]: Returns every messages of the
          given group.
        - iter_message_first(Self,str) -> Message: Returns the first message to
          load for a given group.
        - oldest_message(Self,str) -> Message: Returns the oldest message to
          load for a given group.
        - iter_message_next(Self,Message) -> Message: Returns the message which
          should be loaded after the given message.
        - rename_group(Self,str,str): Rename the given group.
        - remove_user_from_group(Self,str,str): Remove the given user from the
          given group.
        - add_user_to_group(Self,str,str): Adds the given user to the given
          group.
        - create_group(Self,Group) -> str: Creates the given group in the
          database.
        - get_group(Self,str) -> Group: Returns the group with the given id.
        - get_groups_user(Self,str) -> list[Group]: Returns all the group of a
          given user.
        - create_message(Self,Message) -> str: Create a new message in the
          database.
        - create_message_with_medias(Self,Message,list[Media]) -> str: Creates
          a message and its medias in the database.
        - get_message_user_iterator(Self,str) -> Message_iterator: Returns an
          iterator for the messages of a group.
        - get_medias_message(Self,str) -> list[Media]: Returns the medias
          attached to a given message.
        - get_message(Self,str) -> Message:: Returns the message with the given
          id.
        - delete_message(Self,str): Deletes the message with the given id.
        - get_media(Self,str) -> Media:: Returns the media with the given id.
        - create_media(Self,Media,str) -> str: Creates a new media in the
          database.
        - get_media(Self,str) -> Media:: Returns the media with the given id.
        - delete_media(Self,str): Deleted the given media from the database.
        - create_user(Self,User) -> str:: Creates the given user in the
          database.
        - delete_user(Self,str): Delete the given user.
        - get_user(Self,str) -> User:: Returns the user with the given id.
        - get_user_auth(Self,str) -> User:: Returns the user with the given id
          in the authentification database.
        - get_user_email(Self,str) -> User:: Returns the user with the given
          email.
        - set_user(Self,str,User): Changes the given user.
        - get_all_users(Self) -> list[User]: Returns all the users of the
          database.
        - get_users_in_group(Self,str) -> list[User]: Returns the users of a
          group.
        - init_user_iterator(Self) -> Iterator[User]: Returns an iterator over
          all the users.
        - get_next_user(Self,Iterator[User]) -> Optional[User]: Returns the
          next user of the given iterator.
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
            raise DatabaseException(
                    f'Failed to instanciate the database service: {e}'
                    )

    def fetch_query( self: Self, query: str, params: list[Any]=None) -> list[tuple[Any]]:
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

    def get_all_messages_group(self: Self, group_id: str) -> list[Message]:
        """ Returns every messages of the given group.
        ---
        Parameters:
            self (Self): Current instance.
            group_id (str): Id of the group to get the messages of.
        ---
        Returns:
            (list[Message]): List of all the messages of the given group.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        message = service_bdd.get_all_messages_group('group_id')
        ```
        """
        try:
            query_result = self.fetch_query(
                    "SELECT * FROM message "
                    "WHERE receiver_group_id = %s "
                    "ORDER BY date ASC",
                    [group_id]
                    )
        except Exception as e:
            raise DatabaseException(
                    f'Could not execute the query to get all the messages for '
                    f'{group_id=}: {e}'
                    )
        return [Message(*res[1:], id = res[0]) for res in query_result]

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
            user_id: str,
            group_id: str
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
        Parameters:
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
                    [message.get_content(),
                     message.get_sender_id(),
                     message.get_receiver_group_id(),
                     message.get_date()]
                    )
            message.set_id(message_id)
        except Exception as e:
            raise DatabaseException(
                    f'Could not create the message {message}: {e}'
                    )
        return message_id

    def create_message_with_medias(
            self: Self,
            message: Message,
            medias: list[Media]
            ) -> str:
        """ Creates a message and its medias in the database.
        ---
        Parameters:
            self (Self): Current instance.
            message (Message): Message to create.
            medias (list[Media]): List of medias attached to the message.
        ---
        Returns:
            (str): Id of the message in the database.
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
        media = Media(
            'type',
            'link'
            )
        service_bdd = Service_bdd()
        message_id = service_bdd.create_message_with_medias(
                my_message,
                [media]
                )
        ```
        """
        message_id = self.create_message(message)
        for media in medias:
            self.create_media(media, message_id)
        return message_id

    def get_message_user_iterator(
            self: Self,
            group_id: str
            ) -> Message_iterator:
        """ Returns an iterator for the messages of a group.
        ---
        Parameters:
            self (Self): Current instance.
            group_id (str): Group of the id to create an iteraor for.
        ---
        Returns:
            (Message_iterator): Iterator over the messages of the given group.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        for message in service_bdd.get_message_user_iterator('user_id'):
            print(message)
        ```
        """
        return Message_iterator(group_id)

    def get_medias_message(self: Self, message_id: str) -> list[Media]:
        """ Returns the medias attached to a given message.
        ---
        Parameters:
            self (Self): Current instance.
            message_id (str): Id of the message to get the medias from.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Returns:
            (list[Media]): List of medias attached to the given message.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        for media in service_bdd.get_medias_message('message_id'):
            print(media)
        ```
        """
        query = 'SELECT * FROM medias WHERE message_id = %s'
        try:
            medias = self.fetch_query(query, [message_id])
        except Exception as e:
            raise DatabaseException(
                    f'Could not get the medias for '
                    f'the message {message_id}: {e}'
                    )
        return [Media(*line[1:], id = line[0]) for line in medias]

    def get_message(self: Self, message_id: str) -> Message:
        """ Returns the message with the given id.
        ---
        Parameters:
            self (Self): Current instance.
            message_id (str): Id of the message to get.
        ---
        Returns:
            (Message): Message with the given id.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        message = service_bdd.get_message('message_id')
        ```
        """
        query = 'SELECT * FROM messages WHERE id = %s'
        try:
            message = self.fetch_query(query, [message_id])[0]
        except Exception as e:
            raise DatabaseException(
                    f'Could not get the message {message_id}: {e}'
                    )
        return Message(*message[1:], id = message[0])

    def delete_message(self: Self, message_id: str):
        """ Deletes the message with the given id.
        ---
        Parameters:
            self (Self): Current instance.
            message_id (str): Id of the message to delete.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        message = service_bdd.delete_message('message_id')
        ```
        """
        query = 'DELETE FROM messages WHERE id = %s'
        try:
            self.change_query(query, [message_id])
        except Exception as e:
            raise DatabaseException(
                    f'Could not delete the message {message_id}: {e}'
                    )

    def get_media(self: Self, media_id: str) -> Media:
        """ Returns the media with the given id.
        ---
        Parameters:
            self (Self): Current instance.
            media_id (str): Id of the media to get.
        ---
        Returns:
            (Media): Media with the given id.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        media = service_bdd.get_media('media_id')
        ```
        """
        query = 'SELECT * FROM medias WHERE id = %s'
        try:
            media = self.fetch_query(query, [media_id])[0]
        except Exception as e:
            raise DatabaseException(
                    f'Could not get the media {media_id}: {e}'
                    )
        return Media(*media[1:], id = media[0])

    def create_media(
            self: Self,
            media: Media,
            message_id: str
            ) -> str:
        """ Creates a new media in the database.
        ---
        Parameters:
            self (Self): Current instance.
            media (Media): Media to create in the database, will set its id.
            message_id (str): Id of the message that attach the media.
        ---
        Returns:
            (str): Id of the given media.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        media = Media(
            'type',
            'link'
            )
        service_bdd = Service_bdd()
        message_id = service_bdd.create_media(media, 'message_id')
        ```
        """
        query = ('INSERT INTO medias (type_, link, message_id) '
                 'VALUES (%s, %s, %s)')
        try:
            media_id = self.change_query(
                    query,
                    [media.get_type(), media.get_link(), message_id]
                    )
            media.id = media_id
        except Exception as e:
            raise DatabaseException(
                    f'Could not create the media {Media}: {e}'
                    )
        return media_id

    def get_media(self: Self, media_id: str) -> Media:
        """ Returns the media with the given id.
        ---
        Parameters:
            self (Self): Current instance.
            media_id (str): Id of the wanted media.
        ---
        Returns:
            (Media): Media with the given id.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        my_media = service_bdd.get_media('media_id')
        ```
        """
        query = 'SELECT * FROM medias WHERE id = %s'
        try:
            line = self.fetch_query(query, [media_id])[0]
        except Exception as e:
            raise DatabaseException(
                    f'Could not get the media {media_id}: {e}'
                    )
        return Media(*line[1:], id = line[0])

    def delete_media(self: Self, media_id: str):
        """ Deleted the given media from the database.
        ---
        Parameters:
            self (Self): Current instance.
            media_id (str): Id of the media to delete.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        media = Media(
            'type',
            'link'
            )
        service_bdd = Service_bdd()
        message_id = service_bdd.create_media(media, 'message_id')
        service_bdd.delete_media(media_id)
        ```
        """
        query = 'DELETE FROM medias WHERE id = %s'
        try:
            self.change_query(query, [media_id])
        except Exception as e:
            raise DatabaseException(
                    f'Could not delete the media {media_id}: {e}'
                    )

    def create_user(self: Self, user: User) -> str:
        """ Creates the given user in the database.
        ---
        Parameters:
            self (Self): Current instance.
            user (User): User to create. Will receive its id.
        ---
        Returns:
            (str): Id of the user in the database.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        my_user = User(
                'name',
                'first_name',
                'e@mail.com',
                10000,
                'auth_id'
                )
        service_bdd = Service_bdd()
        user_id = service_bdd.create_user(my_user)
        assert(user_id == my_user.get_id())
        ```
        """
        query = ('INSERT INTO users (name, first_name, email, auth_id) '
                 'VALUES (%s, %s, %s, %s) RETURNING id')
        try:
            user_id = self.change_query(
                    query,
                    [user.get_name(),
                     user.get_first_name(),
                     user.get_auth_id()]
                    )[0][0]
            user.set_id(user_id)
        except Exception as e:
            raise DatabaseException(f'Could not create the user {user}: {e}')
        return user_id

    def delete_user(self: Self, user_id: str):
        """ Delete the given user.
        ---
        Parameters:
            self (Self): Current instance.
            user_id (str): Id of the user to delete.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        my_user = User(
                'name',
                'first_name',
                'e@mail.com',
                10000,
                'auth_id'
                )
        service_bdd = Service_bdd()
        user_id = service_bdd.create_user(my_user)
        service_bdd.delete_user(user_id)
        ```
        """
        query = 'DELETE FROM users WHERE id = %s'
        try:
            self.change_query(query, [user_id])
        except Exception as e:
            raise DatabaseException(
                    f'Could not delete the user {user_id}: {e}.'
                    )

    def get_user(self: Self, user_id: str) -> User:
        """ Returns the user with the given id.
        ---
        Parameters:
            self (Self): Current instance.
            user_id (str): Id of the user to return.
        ---
        Returns:
            (User): User with the given id.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        my_user = User(
                'name',
                'first_name',
                'e@mail.com',
                10000,
                'auth_id'
                )
        service_bdd = Service_bdd()
        user_id = service_bdd.create_user(my_user)
        assert(my_user == service_bdd.get_user(user_id))
        ```
        """
        query = 'SELECT * FROM users WHERE id = %s'
        try:
            line = self.fetch_query(query, [user_id])[0]
        except Exception as e:
            raise DatabaseException(
                    f'Could not get the user {user_id}: {e}'
                    )
        return User(*line[1:], id = line[0])

    def get_user_auth(self: Self, auth_id: str) -> User:
        """ Returns the user with the given id in the authentification database.
        ---
        Parameters:
            self (Self): Current instance.
            auth_id (str): Id of the wanted user in the authentification
            database.
        ---
        Returns:
            (User): User with the given auth_id.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        my_user = User(
                'name',
                'first_name',
                'e@mail.com',
                10000,
                'auth_id'
                )
        service_bdd = Service_bdd()
        user_id = service_bdd.create_user(my_user)
        assert(my_user == service_bdd.get_user_auth('auth_id'))
        ```
        """
        query = 'SELECT * FROM users WHERE auth_id = %s'
        try:
            line = self.fetch_query(query, [auth_id])[0]
        except Exception as e:
            raise DatabaseException(
                    f'Could not get the user with {auth_id=}: {e}'
                    )
        return User(*line[1:], id = line[0])

    def get_user_email(self: Self, email: str) -> User:
        """ Returns the user with the given email.
        ---
        Parameters:
            self (Self): Current instance.
            email (str): Email address of the wanted user.
        ---
        Returns:
            (User): User with the given email.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        my_user = User(
                'name',
                'first_name',
                'e@mail.com',
                10000,
                'auth_id'
                )
        service_bdd = Service_bdd()
        user_id = service_bdd.create_user(my_user)
        assert(my_user == service_bdd.get_user_email('e@mail.com'))
        ```
        """
        query = 'SELECT * FROM users WHERE email = %s'
        try:
            line = self.fetch_query(query, [email])[0]
        except Exception as e:
            raise DatabaseException(
                    f'Could not get the user with {email=}: {e}'
                    )
        return User(*line[1:], id = line[0])

    def set_user(self: Self, user_id: str, user: User):
        """ Changes the given user.
        ---
        Parameters:
            self (Self): Current instance.
            user_id (str): Id of the user to change.
            user (User): User with the new values for each column.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        my_user = User(
                'name',
                'first_name',
                'e@mail.com',
                10000,
                'auth_id'
                )
        service_bdd = Service_bdd()
        user_id = service_bdd.create_user(my_user)
        new_values = User(
                'new_name',
                'first_name',
                'email@test.com',
                10000,
                'auth_id'
                )
        user_id = service_bdd.set_user(my_user, new_values)
        ```
        """
        query = ('UPDATE users '
                 'SET name = %s, first_name = %s, '
                 'email = %s WHERE id = %s')
        try:
            self.change_query(
                    query,
                    [user.get_name(),
                     user.get_first_name(),
                     user.get_email(),
                     user_id]
                    )
        except Exception as e:
            raise DatabaseException(
                    f'Error coud not modify the user {user_id} to {user}: {e}.'
                    )

    def get_all_users(self: Self) -> list[User]:
        """ Returns all the users of the database.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (list[User]): List of all the users of the database.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        all_users = service_bdd.get_all_users()
        ```
        """
        query = 'SELECT * FROM users'
        try:
            lines = self.fetch_query(query)
        except Exception as e:
            raise DatabaseException(f'Could not get all the users: {e}.')
        return [User(*line[1:], id = line[0]) for line in lines]

    def get_users_in_group(self: Self, group_id: str) -> list[User]:
        """ Returns the users of a group.
        ---
        Parameters:
            self (Self): Current instance.
            group_id (str): Id of the group to get the users of.
        ---
        Returns:
            (list[User]): List of the users of the given group.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        users = service_bdd.get_users_in_group('group_id')
        ```
        """
        query = ('SELECT users.* FROM users '
                 'JOIN useringroup ON user.id = useringroup.user_id '
                 'WHERE useringroup.group_id = %s')
        try:
            lines = self.fetch_query(query, [group_id])
        except Exception as e:
            raise DatabaseException(
                    f'Could not get all the users of group {group_id}: {e}.'
                    )
        return [User(*line[1:], id = line[0]) for line in lines]

    def init_user_iterator(self: Self) -> Iterator[User]:
        """ Returns an iterator over all the users.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (Iterator[User]): Iterator over all the users of the database.
        ---
        Raises:
            (DatabaseException): If the query fails.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        for user in service_bdd.init_user_iterator():
            print(user)
        ```
        """
        return iter(self.get_all_users())

    def get_next_user(
            self: Self,
            user_iterator: Iterator[User]
            ) -> Optional[User]:
        """ Returns the next user of the given iterator.
        ---
        Parameters:
            self (Self): Current instance.
            user_iterator (Iterator[User]): Iterator over users in the database.
        ---
        Returns:
            (Optional[User]): Next user of the iterator or None if no more
            users.
        ---
        Example:
        ```python
        service_bdd = Service_bdd()
        iterator = service_bdd.init_user_iterator()
        while (user:= self.get_next_user(iterator)) != None:
            print(user)
        ```
        """
        try:
            return next(user_iterator)
        except StopIteration:
            return None
