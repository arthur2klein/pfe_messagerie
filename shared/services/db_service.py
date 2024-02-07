from __future__ import annotations
from typing import Type
from shared.models.message import Message
from shared.exceptions.database_exception import DatabaseException
import psycopg2
from psycopg2 import sql

class Db_service:
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
        db_service = Db_service()
        ```
        """
        self.connection = psycopg2.connect(
                dbname = 'pfe_database',
                user = 'my_user',
                password = 'my_password',
                host = 'postgres',
                port = 5432,
                )
        self.cursor = self.connection.cursor()

    def execute_query(
            self: Self,
            query: str,
            params: list[Any]=None
            ) -> list[tuple[Any]]:
        """ Executes the given query on the database.
        ---
        Parameters:
            query (str): Query to execute, parameters use %s placeholders.
            params (list[Any]): Parameters of the query.
        ---
        Returns:
            (list[typle[Any]]): List of the rows returned by the database for
            the given query.
        ---
        Example:
        ```python
        db_service = Db_service()
        db_service.execute_query(
                "SELECT * FROM Table WHERE name = %s",
                ["name"]
                )
        ```
        """
        self.cursor.execute(sql.SQL(query), params)
        return self.cursor.fetchall()

    def close_connection(self):
        """ Close the connection to the database.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Example:
        ```python
        db_service = Db_service()
        db_service.close_connection()
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
        my_service = Db_service()
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
        db_service = Db_service()
        message = db_service.iter_message_first('3')
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
        db_service = Db_service()
        message = db_service.oldest_message('3')
        ```
        """
        try:
            query_result = self.execute_query(
                    "SELECT * FROM message " \
                    "WHERE receiver_group_id = %s " \
                    "ORDER BY date ASC Limit 1",
                    [group_id]
                    )
        except Exception as e:
            raise DatabaseException(
                    f'Could not execute the query to get the oldest message ' \
                    f'for {group_id=}: {e}'
                    )
        try:
            res = query_result[0]
        except IndexError:
            raise StopIteration('No message found for the given group.')
        return Message.from_json(res)

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
        db_service = Db_service()
        message = db_service.iter_message_first('3')
        next_message = db_service.iter_message_next(message)
        ```
        """
        group_id = current.receiver_group_id
        date = current.date
        try:
            query_result = self.execute_query(
                    "SELECT * FROM message " \
                    "WHERE receiver_group_id = %s " \
                    "AND date > %s " \
                    "ORDER BY date ASC Limit 1",
                    [group_id, date]
                    )
        except Exception as e:
            raise DatabaseException(
                    f'Could not execute the query to get the next message ' \
                    f'for {group_id=}: {e}'
                    )
        try:
            res = query_result[0]
        except IndexError:
            raise StopIteration('No next message found for the given group.')
        return Message.from_json(res)
