from __future__ import annotations
from typing import Type
import json

class Message:
    """ Represents a message that a user send in a group.
    ---
    Attributes:
        id (Optional[str]): Id of the current message as set in the database.
        content (str): Content of the current message.
        sender_id (str): Id of the user who sent the current message.
        receiver_group_id (str): Id of the group of users who received the
        message.
        date (int): Date the message was send at.
    ---
    Methods:
        __eq__(Self, Message) -> bool: Checks for equality between two
        instances.
        __init__(Self, str, str, str, int, Optional[str]): Creates a new
        message.
        __repr__(Self) -> str: Converts the current message to a displayable
        string.
        __str__(Self) -> str: Converts the current message to a string.
        from_json(str) -> Self: Creates a new instance from a json string.
        to_json(Self) -> str: Converts the current instance to a json string.
        get_content(Self) -> str: Returns the content of the current message.
        get_date(Self) -> int: Returns the date the current message was sent at.
        get_id(Self) -> Optional[str]: Returns the id that the database gave to
        the current message.
        get_receiver_group_id(Self) -> str: Returns the id of the group who
        received the message.
        get_sender_id(Self) -> str: Returns the id of the user who sent the
        message.
        set_content(Self, str): Changes the content of the current message.
        set_date(Self, int): Changes the date the current message was sent at.
        set_id(Self, str): Changes the id of the current message.
        set_receiver_group_id(Self, str): Changes the id of the group who
        received the current message.
        set_sender_id(Self, str): Changes the id of the user who sent the
        current message.
    """

    def __init__(
            self: Self,
            content: str,
            sender_id: str,
            receiver_group_id: str,
            date: int,
            id: Optional[str] = None
            ):
        """ Creates a new message with the given attirbutes.
        ---
        Parameters:
            self (Self): Current instance.
            content (str): Content of the current message.
            sender_id (str): Id of the user who sends the message.
            receiver_group_id (str): Id of the group that receive the message.
            date (int): Date the message was sent at.
            id (Optional[str]): Id that the message gives to the message.
        ---
        Example:
        ```python
        message = Message(
            'Hello world!',
            '1',
            '2',
            1706873888
        )
        ```
        """
        self.id = id
        self.content = content
        self.sender_id = sender_id
        self.receiver_group_id = receiver_group_id
        self.date = date

    def __eq__(self: Self, other: Message) -> bool:
        """ Check for equality between two instances.
        ---
        Parameters:
            self (Self): Current instance.
            other (Group): Instance to compare to.
        ---
        Returns:
            (bool): True iff the two instances have the same attributes.
        ---
        Example:
        ```python
        ```
        """
        if not(isinstance(other, Message)):
            return False
        return (self.content == other.content and
                self.sender_id == other.sender_id and
                self.receiver_group_id == other.receiver_group_id and
                self.date == other.date and
                self.id == other.id)

    @staticmethod
    def from_json(json_string: str) -> Self:
        """ Create a new instance with the attributes given in a json formatted
        string.
        ---
        Parameters:
            json_string (str): Json string that contains the values of the
            attributes of a new Media.
        ---
        Returns:
            (Self): New media with the values of the given json.
        ---
        Example:
        ```python
        target = Message(
                content = 'Hello world!',
                sender_id = '1',
                receiver_group_id = '2',
                date = 1706873888
                )
        message_json = '{ ' \
                '"content": "Hello world!", ' \
                '"sender_id": "1", ' \
                '"receiver_group_id": "2", ' \
                '"date": 1706873888}'
        message = Message.from_json(message_json)
        assert(message == target)
        ```
        """
        attributes = json.loads(json_string)
        return Message(**attributes)

    def to_json(self: Self) -> str:
        """ Converts the current instance to a json string.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (str): Json string containing the attributes of the current
            instance.
        ---
        Example:
        ```python
        message = Message(
                content = 'Hello world!',
                sender_id = '1',
                receiver_group_id = '2',
                date = 1706873888
                )
        target = '{' \
                '"content": "Hello world!", ' \
                '"sender_id": "1", ' \
                '"receiver_group_id": "2", ' \
                '"date": 1706873888}'
        message_json = message.to_json()
        assert(message_json == target)
        ```
        """
        if self.id == None:
            id_part = ''
        else:
            id_part = f'"id": "{self.id}", '
        return f'{{' \
                f'{id_part}"content": "{self.content}", ' \
                f'"sender_id": "{self.sender_id}", ' \
                f'"receiver_group_id": "{self.receiver_group_id}", ' \
                f'"date": {self.date}' \
                f'}}'

    def __repr__(self: Self) -> str:
        """ Convert the current instance to a displayable string.
        The id field is absent if None.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (str): Attributes of the current instance in a json-formatted
            string.
        """
        return self.to_json()

    def __str__(self: Self) -> str:
        """ Convert the current instance to a json string.
        The id field is absent if None.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (str): Attributes of the current instance in a json-formatted
            string.
        ---
        Example:
        ```python
        message = Message(
                content = 'Hello world!',
                sender_id = '1',
                receiver_group_id = '2',
                date = 1706873888,
                id = '4'
                )
        target = '{"id": "4", ' \
                '"content": "Hello world!", ' \
                '"sender_id": "1", ' \
                '"receiver_group_id": "2", ' \
                '"date": 1706873888}'
        message_json = str(message)
        assert(message_json == target)
        """
        return self.to_json()

    def get_content(self: Self) -> str:
        """ Returns the content of the current message.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (str): Content of the current message.
        ---
        Example:
        ```python
        message = Message(
                content = 'Hello world!',
                sender_id = '1',
                receiver_group_id = '2',
                date = 1706873888,
                id = '4'
                )
        assert(message.get_content() == 'Hello world!')
        ```
        """
        return self.content

    def get_sender_id(self: Self) -> str:
        """ Returns the id of the user who sent the current message.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (str): Id of the sender of the current message.
        ---
        Example:
        ```python
        message = Message(
                content = 'Hello world!',
                sender_id = '1',
                receiver_group_id = '2',
                date = 1706873888,
                id = '4'
                )
        assert(message.get_sender_id() == '1')
        ```
        """
        return self.sender_id

    def get_receiver_group_id(self: Self) -> str:
        """ Returns the id of the group which received the current message.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (str): Id of the group which received the current message.
        ---
        Example:
        ```python
        message = Message(
                content = 'Hello world!',
                sender_id = '1',
                receiver_group_id = '2',
                date = 1706873888,
                id = '4'
                )
        assert(message.get_receiver_group_id() == '2')
        ```
        """
        return self.receiver_group_id

    def get_date(self: Self) -> str:
        """ Returns the date the message was sent at.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (str): Date the message was sent at.
        ---
        Example:
        ```python
        message = Message(
                content = 'Hello world!',
                sender_id = '1',
                receiver_group_id = '2',
                date = 1706873888,
                id = '4'
                )
        assert(message.get_date() == 1706873888)
        ```
        """
        return self.date

    def get_id(self: Self) -> Optional[str]:
        """ Returns the id that the database gave to the message or None if it
        is not known.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (str): Id that the database gave to the message or None if it is
            not known.
        ---
        Example:
        ```python
        message = Message(
                content = 'Hello world!',
                sender_id = '1',
                receiver_group_id = '2',
                date = 1706873888,
                id = '4'
                )
        assert(message.get_id() == '4')
        ```
        """
        return self.id

    def set_content(self: Self, new_content: str):
        """ Changes the content of the current message.
        ---
        Parameters:
            self (Self): Current instance.
            new_content (str): New content of the message.
        ---
        Example:
        ```python
        message = Message(
                content = 'Hello world!',
                sender_id = '1',
                receiver_group_id = '2',
                date = 1706873888,
                id = '4'
                )
        assert(message.get_content() == 'Hello world!')
        message.set_content('test')
        assert(message.get_content() == 'test')
        ```
        """
        self.content = new_content

    def set_sender_id(self: Self, new_sender_id: str):
        """ Changes the id of the user who sent the message.
        ---
        Parameters:
            self (Self): Current instance.
            new_sender_id (str): Id of the new user who sent the message.
        ---
        Example:
        ```python
        message = Message(
                content = 'Hello world!',
                sender_id = '1',
                receiver_group_id = '2',
                date = 1706873888,
                id = '4'
                )
        assert(message.get_sender_id() == '1')
        message.set_sender_id('2')
        assert(message.get_sender_id() == '2')
        ```
        """
        self.sender_id = new_sender_id

    def set_receiver_group_id(self: Self, new_receiver_group_id: str):
        """ Changes the id of the group who received the message.
        ---
        Parameters:
            self (Self): Current instance.
            new_receiver_group_id (str): Id of the new group who received the
            message.
        ---
        Example:
        ```python
        message = Message(
                content = 'Hello world!',
                sender_id = '1',
                receiver_group_id = '2',
                date = 1706873888,
                id = '4'
                )
        assert(message.get_receiver_group_id() == '2')
        message.set_receiver_group_id('3')
        assert(message.get_receiver_group_id() == '3')
        ```
        """
        self.receiver_group_id = new_receiver_group_id

    def set_date(self: Self, new_date: str):
        """ Changes the date the message was sent at.
        ---
        Parameters:
            self (Self): Current instance.
            new_date: Date the message was sent at.
        ---
        Example:
        ```python
        message = Message(
                content = 'Hello world!',
                sender_id = '1',
                receiver_group_id = '2',
                date = 1706873888,
                id = '4'
                )
        assert(message.get_date() == 1706873888)
        message.set_date(1706873898)
        assert(message.get_date() == 1706873898)
        ```
        """
        self.date = new_date

    def set_id(self: Self, new_id: str):
        """ Changes the id of the message.
        ---
        Parameters:
            self (Self): Current instance.
            new_date: New id of the message.
        ---
        Example:
        ```python
        message = Message(
                content = 'Hello world!',
                sender_id = '1',
                receiver_group_id = '2',
                date = 1706873888,
                id = '4'
                )
        assert(message.get_id() == '4')
        message.set_id('5')
        assert(message.get_id() == '5')
        ```
        """
        self.id = new_id
