from __future__ import annotations
from typing import Type
import json

class User:
    """ Represents a user of the application.
    ---
    Attributes:
        id (Optional[str]): Id of the user in the database.
        name (str): Name of the user.
        first_name (str): First name of the user.
        email (str): Email of the user.
        join_date (int): Join date of the user.
        auth_id (Optional[str]): Id of user for the authentification service.
    ---
    Methods:
        __eq__(Self, User) -> bool: Check for equality in the attributes.
        __init__(str, str, str, int, Optional[str], Optional[str]): Creates a
        new instance.
        __repr__(Self) -> str: Convert the instance to a displayable string.
        __str__(Self) -> str: Convert the instance to a string.
        from_json(str) -> Self: Create a new instance with the values of a json
        string.
        to_json(Self) -> str: Converts the current instance to a json string.
        get_auth_id(Self) -> Optional[str]: Returns the id of the user for the
        authentification service.
        get_email(Self) -> str: Returns the email address of the current user.
        get_first_name(Self) -> str: Returns the first name of the current user.
        get_id(Self) -> Optional[str]: Returns the id of the current user.
        get_join_date(Self) -> int: Returns the join date of the current user.
        get_name(Self) -> str: Returns the name of the current user.
        set_auth_id(Self, str): Modify the id of the current user for the
        authentification service.
        set_email(Self, str): Modify the email address of the current user.
        set_first_name(Self, str): Modifiy the first name of the current user.
        set_id(Self, str): Modify the id of the current user.
        set_name(Self, str): Modify the name of the current user.
    """

    def __init__(
        self: Self,
        name: str,
        first_name: str,
        email: str,
        join_date: int,
        auth_id: Optional[str] = None,
        id: Optional[str] = None,
    ):
        """ Creates a new User.
        ---
        Parameters:
            id (Optional[str]): Id of the user in the database.
            name (str): Name of the user.
            first_name (str): First name of the user.
            email (str): Email of the user.
            join_date (int): Join date of the user.
            auth_id (Optional[str]): Id of user for the authentification service.
        ---
        Example:
        ```python
        my_user = User(
            'my_name',
            'my_first_name',
            'my_email',
            1706873888
        )
        other_User = User(
            'my_name',
            'my_first_name',
            'my_email',
            1706873888,
            id = '5',
            auth_id = '4'
        )
        """
        self.name = name
        self.first_name = first_name
        self.email = email
        self.join_date = join_date
        self.id = id
        self.auth_id = auth_id

    def __eq__(self: Self, other: User) -> bool:
        """ Check for equality between two instances of User.
        Compares the values of the attributes except auth_id.
        ---
        Parameters:
            self (Self): Current instance.
            other (User): User to compare to.
        ---
        Returns:
            (bool): True iff the two instances have same attributes without
            taking auth_id into account.
        ---
        Example:
        ```python
        user1 = User(
            'my_name',
            'my_first_name',
            'my_email',
            1706873888
        )
        user2 = User(
            'my_name',
            'my_first_name',
            'my_email',
            1706873888,
            auth_id = '4'
        )
        user3 = User(
            'myname',
            'myfirstname',
            'myemail',
            1706873888
        )
        assert(user1 == user2)
        assert(user1 != user3)
        ```
        """
        if not(isinstance(other, User)):
            return False
        return (
            self.name == other.name and
            self.first_name == other.first_name and
            self.email == other.email and
            self.join_date == other.join_date and
            self.id == other.id
        )

    def __str__(self: Self) -> str:
        """ Converts the current instance to a json string.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (str): Json formatted string containing all not-None attributes.
        ---
        Example:
        ```python
        user1 = User(
            'my_name',
            'my_first_name',
            'my_email',
            1706873888
        )
        assert(
            str(user1) ==
            '{' \
                '"name": "my_name", ' \
                '"first_name": "my_first_name", ' \
                '"email": "my_email", ' \
                '"join_date": 1706873888' \
            '}'
        )
        user2 = User(
            'my_name',
            'my_first_name',
            'my_email',
            1706873888,
            id = '5',
            auth_id = '4'
        )
        assert(
            str(user2) ==
            '{' \
                '"id": "5", ' \
                '"name": "my_name", ' \
                '"first_name": "my_first_name", ' \
                '"email": "my_email", ' \
                '"join_date": 1706873888, ' \
                '"auth_id": "4"' \
            '}'
        )
        ```
        """
        return self.to_json()

    def to_json(self: Self) -> str:
        """ Converts the current instance to a json string.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (str): Json formatted string containing all not-None attributes.
        ---
        Example:
        ```python
        user1 = User(
            'my_name',
            'my_first_name',
            'my_email',
            1706873888
        )
        assert(
            user1.to_json() ==
            '{' \
                '"name": "my_name", ' \
                '"first_name": "my_first_name", ' \
                '"email": "my_email", ' \
                '"join_date": 1706873888' \
            '}'
        )
        user2 = User(
            'my_name',
            'my_first_name',
            'my_email',
            1706873888,
            id = '5',
            auth_id = '4'
        )
        assert(
            user2.to_json() ==
            '{' \
                '"id": "5", ' \
                '"name": "my_name", ' \
                '"first_name": "my_first_name", ' \
                '"email": "my_email", ' \
                '"join_date": 1706873888, ' \
                '"auth_id": "4"' \
            '}'
        )
        ```
        """
        if self.id == None:
            id_part = ''
        else:
            id_part = f'"id": "{self.id}", '
        if self.auth_id == None:
            auth_id_part = ''
        else:
            auth_id_part = f', "auth_id": "{self.auth_id}"'
        return f'{{{id_part}"name": "{self.name}", ' \
               f'"first_name": "{self.first_name}", ' \
               f'"email": "{self.email}", ' \
               f'"join_date": {self.join_date}{auth_id_part}}}'

    def __repr__(self: Self) -> str:
        """ Converts the current instance to a displayable string.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (str): Json formatted string containing all not-None attributes.
        """
        return str(self)

    @staticmethod
    def from_json(json_string: str) -> Self:
        """ Convert a json string to a new instance of User.
        ---
        Parameters:
            json_string (str): Json formatted string with a name field and
            two optional fields id and auth_id.
        ---
        Returns:
            (Self): New instance of User with the wanted attributes values.
        ---
        Example:
        ```python
        user_json = '{' \
            '"name": "my_name", ' \
            '"first_name": "my_first_name", ' \
            '"email": "my_email", ' \
            '"join_date": 1706873888 ' \
        '}'
        assert(
            User.from_json(user_json) == \
            User(
                "my_name",
                "my_first_name",
                "my_email",
                1706873888
            )
        )
        user_json = '{' \
            '"id": "5", ' \
            '"name": "my_name", ' \
            '"first_name": "my_first_name", ' \
            '"email": "my_email", ' \
            '"join_date": 1706873888, ' \
            '"auth_id": "4"' \
        '}'
        assert(
            User.from_json(user_json) == \
            User(
                "my_name",
                "my_first_name",
                "my_email",
                1706873888,
                id = "5",
                auth_id = "4"
            )
        )
        ```
        """
        attributes = json.loads(json_string)
        return User(**attributes)
    
    def get_name(self: Self) -> str:
        """ Returns the name of the current user.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (str): Name of the current user.
        ---
        Example:
        ```python
        user = User(
            "my_name",
            "my_first_name",
            "my_email",
            1706873888,
            id = "5",
            auth_id = "4"
        )
        assert(user.get_name() == "my_name")
        ```
        """
        return self.name

    def get_first_name(self: Self) -> str:
        """ Returns the first name of the current user.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (str): First name of the current user.
        ---
        Example:
        ```python
        user = User(
            "my_name",
            "my_first_name",
            "my_email",
            1706873888,
            id = "5",
            auth_id = "4"
        )
        assert(user.get_first_name() == "my_first_name")
        ```
        """
        return self.first_name
    
    def get_email(self: Self) -> str:
        """ Returns the email of the current user.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (str): Email address of the current user.
        ---
        Example:
        ```python
        user = User(
            "my_name",
            "my_first_name",
            "my_email",
            1706873888,
            id = "5",
            auth_id = "4"
        )
        assert(user.get_email() == "my_email")
        ```
        """
        return self.email

    def get_join_date(self: Self) -> int:
        """ Returns the join date of the current user.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (int): Join date of the current user as an int.
        ---
        Example:
        ```python
        user = User(
            "my_name",
            "my_first_name",
            "my_email",
            1706873888,
            id = "5",
            auth_id = "4"
        )
        assert(user.get_join_date() == 1706873888)
        ```
        """
        return self.join_date

    def get_id(self: Self) -> Optional[str]:
        """ Returns the id of the current user.
        The id is generally defined by the database.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (Optional[str]): Id of the current user or None if not defined.
        ---
        Example:
        ```python
        user = User(
            "my_name",
            "my_first_name",
            "my_email",
            1706873888,
        )
        assert(user.get_id() == None)
        user = User(
            "my_name",
            "my_first_name",
            "my_email",
            1706873888,
            id = "5",
            auth_id = "4"
        )
        assert(user.get_id() == '5')
        ```
        """
        return self.id

    def get_auth_id(self: Self) -> Optional[str]:
        """ Returns the id of the current user for the authentification service.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (Optional[str]): Id of the current user for the authentification
            service or None if not defined.
        ---
        Example:
        ```python
        user = User(
            "my_name",
            "my_first_name",
            "my_email",
            1706873888,
        )
        assert(user.get_auth_id() == None)
        user = User(
            "my_name",
            "my_first_name",
            "my_email",
            1706873888,
            id = "5",
            auth_id = "4"
        )
        assert(user.get_auth_id() == '4')
        ```
        """
        return self.auth_id

    def set_name(self: Self, new_name: str):
        """ Modify the name of the current user.
        ---
        Parameters:
            self (Self): Current instance
            new_name (str): New name of the user.
        ---
        Example:
        ```python
        user = User(
            "my_name",
            "my_first_name",
            "my_email",
            1706873888,
            id = "5",
            auth_id = "4"
        )
        assert(user.get_name() == 'my_name')
        user.set_name('new_name')
        assert(user.get_name() == 'new_name')
        ```
        """
        self.name = new_name

    def set_first_name(self: Self, new_first_name: str):
        """ Modify the first name of the current user.
        ---
        Parameters:
            self (Self): Current instance
            new_first_name (str): New first name of the user.
        ---
        Example:
        ```python
        user = User(
            "my_name",
            "my_first_name",
            "my_email",
            1706873888,
            id = "5",
            auth_id = "4"
        )
        assert(user.get_first_name() == 'my_first_name')
        user.set_first_name('new_first_name')
        assert(user.get_first_name() == 'new_first_name')
        ```
        """
        self.first_name = new_first_name

    def set_email(self: Self, new_email: str):
        """ Modify the email address of the current user.
        ---
        Parameters:
            self (Self): Current instance
            new_email (str): New email address of the user.
        ---
        Example:
        ```python
        user = User(
            "my_name",
            "my_first_name",
            "my_email",
            1706873888,
            id = "5",
            auth_id = "4"
        )
        assert(user.get_email() == 'my_email')
        user.set_email('new_email')
        assert(user.get_email() == 'new_email')
        ```
        """
        self.email = new_email

    def set_id(self: Self, new_id: str):
        """ Modify the id of the current user.
        ---
        Parameters:
            self (Self): Current instance
            new_id (int): New id of the user.
        ---
        Example:
        ```python
        user = User(
            "my_name",
            "my_first_name",
            "my_email",
            1706873888,
            auth_id = "4"
        )
        assert(user.get_id() == None)
        user.set_id('5')
        assert(user.get_id() == '5')
        ```
        """
        self.id = new_id

    def set_auth_id(self: Self, new_auth_id: str):
        """ Modify the id of the current user for the authentification service.
        ---
        Parameters:
            self (Self): Current instance
            new_auth_id (int): New id of the user for the authentification service.
        ---
        Example:
        ```python
        user = User(
            "my_name",
            "my_first_name",
            "my_email",
            1706873888,
        )
        assert(user.get_auth_id() == None)
        user.set_auth_id('5')
        assert(user.get_auth_id() == '5')
        ```
        """
        self.auth_id = new_auth_id
