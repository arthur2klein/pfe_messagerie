from __future__ import annotations
from typing import Type
import json
from shared.models.user import User

class Group:
    """ Represents a group of people able to discuss with each other.
    ---
    Attributes:
        id (Optional[str]): Id of the group in the database.
        name (str): Name of the group.
        l_users (list[User]): List of users in the group.
    ---
    Methods:
        __eq__(Self, Other) -> bool: Check for equality between two groups.
        __init__(Self, str, Optional[str]): Create a new group.
        __repr__(Self) -> str: Convert the instance to a displayable string.
        __str__(Self) -> str: Convert the instance to a string.
        from_json(str) -> Self: Convert a json string to a new goup.
        get_id(Self) -> Optional[str]: Returns the id of the current group.
        get_name(Self) -> str: Returns the name of the current group.
        get_id(Self, Optional[str]): Modify the id of the current group.
        get_name(Self, str): Modify the name of the current group.
        to_json(Self) -> str: Convert a group to a json string.
        add_user(Self, User): Adds a new user in the group.
        contains_user(Self, User) -> bool: Check if the given user is in the
        current group.
        get_users(Self) -> Iterator[User]: Returns an iterator over the users
        of the current group.
        remove_user(Self, User) -> bool: Remove the given user from the group
        and return True iff the user was found.
        set_users(Self, list[User]): Modify the list of user with a copy of the
        given list.
    """

    def __init__(
        self: Self,
        name: str,
        id: Optional[str] = None,
        l_users: list[User] = []
    ):
        """ Returns a discussion group.
        id will generally be set by the database.
        ---
        Parameters:
            self (Self): Current instance.
            name (str): Name of the new group.
            id (Optional[str]): Id of the new group, generally set by the
            database.
            l_users (list[User]): List of users in the group.
        ---
        Example:
        ```python
        group_name = 'my_group'
        new_group = Group(group_name)
        """
        self.id = id
        self.name = name
        self.l_users = l_users

    def __eq__(self: Self, other: Other) -> bool:
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
        group1 = Group('my_group', 'id')
        group2 = Group('my_group', 'id')
        group3 = Group('my_group')
        group3 = Group('group', 'id')
        assert(group1 == group2)
        assert(group1 != group2)
        assert(group1 != group3)
        ```
        """
        if not(isinstance(other, Group)):
            return False
        return self.id == other.id and self.name == other.name
        
    def get_id(self: Self) -> Optional[str]:
        """ Returns the id of the current group.
        Returns None if no id has been defined.
        ---
        Parameters:
            self (Self): Current instance
        ---
        Returns:
            (Optional[str]): id of the current group or None if not set.
        ---
        Example:
        ```python
        group_name = 'my_group'
        new_group1 = Group(group_name)
        assert(new_group1.get_id() == None)
        new_group2 = Group(group_name, id = '5')
        assert(new_group2.get_id() == '5')
        ```
        """
        return self.id

    def get_name(self: Self) -> str:
        """ Returns the name of the current group.
        ---
        Parameters:
            self (Self): Current instance
        ---
        Returns:
            (str): name of the current group.
        ---
        Example:
        ```python
        group_name = 'my_group'
        new_group = Group(group_name)
        assert(new_group.get_name() == group_name)
        ```
        """
        return self.name

    def set_id(self: Self, new_id: Optional[str]):
        """ Modify the id of the current group.
        ---
        Parameters:
            self (Self): Current instance
            new_id (Optional[str]): New id of the current group.
        ---
        Example:
        ```python
        group_name = 'my_group'
        new_group = Group(group_name)
        assert(new_group.get_id() == None)
        new_group.set_id('5')
        assert(new_group.get_id() == '5')
        ```
        """
        self.id = new_id

    def set_name(self: Self, name: str):
        """ Modify the name of the current group.
        ---
        Parameters:
            self (Self): Current instance
            new_name (str): name of the current group.
        ---
        Example:
        ```python
        group_name = 'my_group'
        new_group = Group(group_name)
        assert(new_group.get_name() == group_name)
        new_name = 'my_group_'
        new_group.set_name(new_name)
        assert(new_group.get_name() == group_name)
        ```
        """
        return self.name

    def to_json(self: Self) -> str:
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
        group_name = 'my_group'
        new_group1 = Group(group_name)
        json_group1 = new_group1.to_json()
        assert(json_group1 == '{"name": "my_group"}')
        new_group2 = Group(group_name, id = '5')
        json_group2 = new_group2.to_json()
        assert(json_group2 == '{"id": "5", "name": "my_group"}')
        ```
        """
        if self.id == None:
            id_part = ''
        else:
            id_part =  f'"id": "{self.id}", '
        if self.l_users == []:
            users_part = ''
        else:
            users_part =  f', "l_users": ' \
                          f'"{[user.to_json() for user in self.l_users]}"'
        return f'{{{id_part}"name": "{self.name}"{users_part}}}'

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
        group_name = 'my_group'
        new_group1 = Group(group_name)
        str_group1 = str(new_group1)
        assert(str_group1 == '{"name": "my_group"}')
        new_group2 = Group(group_name, id = '5')
        str_group2 = str(new_group2)
        assert(str_group2 == '{"id": "5", "name": "my_group"}')
        ```
        """
        return self.to_json()

    @staticmethod
    def from_json(json_string: str) -> Self:
        """ Convert a json string to a new instance of Group.
        ---
        Parameters:
            json_string (str): Json formatted string with a name field and an
            optional id field.
        ---
        Returns:
            (Self): New instance of Group with the wanted attributes values.
        ---
        Example:
        ```python
        json_string1 = '{"name": "my_group"}'
        new_group1 = Group.from_json(json_string1)
        assert(new_group1 == Group('my_group'))
        json_string2 = '{"id": "5", "name": "my_group"}'
        new_group2 = Group.from_json(json_string2)
        assert(new_group2 == Group('my_group', id = '5'))
        ```
        """
        attributes = json.loads(json_string)
        return Group(**attributes)

    def get_users(self: Self) -> Iterator[User]:
        """ Returns an iterator over the users of the group.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (Iterator[User]): Iterator over the users of the current group.
        ---
        Exmaple:
        ```python
        user = User('name', 'first_name', 'email', 0)
        group = Group('my_group', l_users = [user])
        assert(list(group.get_users()) == [user])
        ```
        """
        return iter(self.l_users)

    def set_users(self: Self, new_l_users: list[User]):
        """ Empty the list of users and copy the users of the given list into
        the new users list.
        ---
        Parameters:
            self (Self): Current instance.
            new_l_users (list[User]): List of new users of the group.
        ---
        Example:
        ```python
        user = User('name', 'first_name', 'email', 0)
        group = Group('my_group')
        assert(list(group.get_users()) == [])
        group.set_users([user])
        assert(list(group.get_users()) == [user])
        ```
        """
        self.l_users = new_l_users[:]

    def add_user(self: Self, user: User):
        """ Add the given user to the current group.
        ---
        Parameters:
            self (Self): Current instance.
            user (User): User to add to the group.
        ---
        Example:
        ```python
        user = User('name', 'first_name', 'email', 0)
        group = Group('my_group')
        assert(list(group.get_users()) == [])
        group.add_user(user)
        assert(list(group.get_users()) == [user])
        ```
        """
        self.l_users.append(user)

    def remove_user(self: Self, user: User) -> bool:
        """ Remove the given user from the current group.
        ---
        Parameters:
            self (Self): Current instance.
            user (User): User to remove to the group.
        ---
        Returns:
            (bool): True iff the given user could be found and remove from the
            group.
        ---
        Example:
        ```python
        user = User('name', 'first_name', 'email', 0)
        group = Group('my_group', l_users = [user])
        assert(list(group.get_users()) == [user])
        assert(group.remove_user(user))
        assert(list(group.get_users()) == [])
        assert(not(group.remove_user(user)))
        ```
        """
        try:
            self.l_users.remove(user)
        except ValueError:
            return False
        return True

    def contains_user(self:  Self, user: User) -> bool:
        """ Checks if the given user is in the current group.
        ---
        Parameters:
            self (Self): Current instance.
            user (User): User to search in the group.
        ---
        Returns:
            (bool): True iff the user is in the current group.
        ---
        Example:
        ```python
        user = User('name', 'first_name', 'email', 0)
        group = Group('my_group')
        assert(not(group.contains_user(user)))
        group.add_user(user)
        assert(group.contains_user(user))
        ```
        """
        return user in self.l_users
