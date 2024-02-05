from __future__ import annotations
from typing import Type
import json

class Media:
    """ Represents a media sent with a message.
    ---
    Attributes:
        id (Optional[str]): Id of the media in the database.
        name (str): Name given to the media.
        type_ (str): Type of the media.
        link (str): Url of the media.
        message_id (str): Id of the message to which the media is attached.
    ---
    Methods:
        __eq__(Self, Media) -> bool: Check for equality between to instances.
        __init__(Self, str, str, str, str, Optional[str]): Creates a new
        instance.
        __repr__(Self) -> str: Converts the media to a displayable string.
        __str__(Self) -> str: Converts the media to a string.
        from_json(str) -> Self: Converts a json string to a new media.
        to_json(Self) -> str: Converts the current instance to a json string.
        get_id(Self) -> Optional[str]: Returns the id of the current media.
        get_link(Self) -> str: Returns the link to the current media.
        get_message_id(Self) -> str: Returns the id of the message the media is
        linked to.
        get_name(Self) -> str: Returns the name of the current media.
        get_type(Self) -> str: Returns the type of media of the current
        instance.
        set_id(Self, str): Changes the id of the current instance.
        set_link(Self, str): Changes the link of the current media.
        set_message_id(Self, str): Changes the id of the message the media is
        linked to.
        set_name(Self, str): Changes the name of the current media.
        set_type(Self, str): Changes the type of media of the current instance.
    """

    def __init__(
            self: Self,
            name: str,
            type_: str,
            link: str,
            message_id: str,
            id: Optional[str] = None
            ):
        """ Returns a new media.
        id will generally be set by the database.
        ---
        Parameters:
            self (Slef): Current instance.
            name (str): Name of the media.
            type_ (str): Type of the media.
            link (str): Link to the media.
            message_id (str): Id of the message to which the media is attached.
            id (Optional[str]): Id of the media as set by the database.
        ---
        Example:
        ```python
        new_media = Media('mon_image', 'img', 'link/to/image.png', '3')
        ```
        """
        self.name = name
        self.type_ = type_
        self.link = link
        self.message_id = message_id
        self.id = id

    def __eq__(self: Self, other: Media) -> bool:
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
        media1 = Media('mon_image', 'img', 'link/to/image.png', '3')
        media2 = Media('mon_image', 'img', 'link/to/image.png', '3')
        media3 = Media('mon_image', 'img', 'link/to/img.png', '3')
        assert(media1 == media2)
        assert(media1 != media3)
        ```
        """
        if not(isinstance(other, Media)):
            return False
        return (self.name == other.name and
                self.type_ == other.type_ and
                self.link == other.link and
                self.message_id == other.message_id and
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
        target = Media('mon_image', 'img', 'link/to/image.png', '3')
        media_json = '{ ' \
                '"name": "mon_image", ' \
                '"type_": "img", ' \
                '"link": "link/to/image.png", ' \
                '"message_id": "3"}'
        media = Media.from_json(media_json)
        assert(media == target)
        ```
        """
        attributes = json.loads(json_string)
        return Media(**attributes)

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
        media = Media('mon_image', 'img', 'link/to/image.png', '3', id = '4')
        target = '{"id": "4", ' \
                '"name": "mon_image", ' \
                '"type_": "img", ' \
                '"link": "link/to/image.png", ' \
                '"message_id": "3"}'
        media_json = media.to_json()
        assert(media_json == target)
        ```
        """
        if self.id == None:
            id_part = ''
        else:
            id_part = f'"id": "{self.id}", '
        return f'{{' \
               f'{id_part}"name": "{self.name}", ' \
               f'"type_": "{self.type_}", ' \
               f'"link": "{self.link}", ' \
               f'"message_id": "{self.message_id}"' \
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
        media = Media('mon_image', 'img', 'link/to/image.png', '3', id = '4')
        target = '{"id": "4", ' \
                '"name": "mon_image", ' \
                '"type_": "img", ' \
                '"link": "link/to/image.png", ' \
                '"message_id": "3"}'
        media_json = media.to_json()
        assert(media_json == target)
        ```
        """
        return self.to_json()

    def get_id(self: Self) -> Optional[str]:
        """ Returns the id of the current instance.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (Optional[str]): Id of the current instance.
        ---
        Example:
        ```python
        media = Media('mon_image', 'img', 'link/to/image.png', '3', id = '4')
        assert(media.get_id() == '4')
        ```
        """
        return self.id

    def get_name(self: Self) -> str:
        """ Returns the name of the current instance.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (str): Name of the current instance.
        ---
        Example
        ```python
        media = Media('mon_image', 'img', 'link/to/image.png', '3', id = '4')
        assert(media.get_name() == 'mon_image')
        ```
        """
        return self.name

    def get_type(self: Self) -> str:
        """ Returns the type of media of the current instance.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (str): Type of the media.
        ---
        Example:
        ```python
        media = Media('mon_image', 'img', 'link/to/image.png', '3', id = '4')
        assert(media.get_type() == 'img')
        ```
        """
        return self.type_

    def get_link(self: Self) -> str:
        """ Returns the link to the cuurent instance.
        ---
        Parameters:
            self (Self): Current instance.
        --- Returns:
            (str): Link to the media.
        ---
        Example:
        ```python
        media = Media('mon_image', 'img', 'link/to/image.png', '3', id = '4')
        assert(media.get_link() == 'link/to/image.png')
        ```
        """
        return self.link

    def get_message_id(self: Self) -> str:
        """ Returns the id of the message associated with the current instance.
        ---
        Parameters:
            self (Self): Current instance.
        --- Returns:
            (str): Message to which the media is attached.
        ---
        Example:
        ```python
        media = Media('mon_image', 'img', 'link/to/image.png', '3', id = '4')
        assert(media.get_message_id() == '3')
        ```
        """
        return self.message_id

    def set_id(self: Self, new_id: str):
        """ Changes the id of the current instance.
        ---
        Parameters:
            self (Self): Current instance.
            new_id (str): New id of the current instance.
        ---
        Example:
        ```python
        media = Media('mon_image', 'img', 'link/to/image.png', '3')
        assert(media.get_id() == None)
        media.set_id('4')
        assert(media.get_id() == '4')
        ```
        """
        self.id = new_id

    def set_name(self: Self, new_name: str):
        """ Changes the name of the current instance.
        ---
        Parameters:
            self (Self): Current instance.
            new_name (str): New name of the current media.
        ---
        Example:
        ```python
        media = Media('mon_image', 'img', 'link/to/image.png', '3')
        assert(media.get_name() == 'mon_image')
        media.set_name('new_name')
        assert(media.get_name() == 'new_name')
        ```
        """
        self.name = new_name

    def set_type(self: Self, new_type: str):
        """ Changes the type of the current instance.
        ---
        Parameters:
            self (Self): Current instance.
            new_type (str): New type of the current media.
        ---
        Example:
        ```python
        media = Media('mon_image', 'img', 'link/to/image.png', '3')
        assert(media.get_type() == 'img')
        media.set_type('audio')
        assert(media.get_type() == 'audio')
        ```
        """
        self.type_ = new_type

    def set_link(self: Self, new_link: str):
        """ Changes the type of the current instance.
        ---
        Parameters:
            self (Self): Current instance.
            new_type (str): New type of the current media.
        ---
        Example:
        ```python
        media = Media('mon_image', 'img', 'link/to/image.png', '3')
        assert(media.get_link() == 'link/to/image.png')
        media.set_link('link/to/img.png')
        assert(media.get_link() == 'link/to/img.png')
        ```
        """
        self.link = new_link

    def set_message_id(self: Self, new_message_id: str):
        """ Changes the id of the message the media is linked to.
        ---
        Parameters:
            self (Self): Current instance.
            new_message_id (str): Id of the message the media will be linked to.
        ---
        Example:
        ```python
        media = Media('mon_image', 'img', 'link/to/image.png', '3')
        assert(media.get_message_id() == '3')
        media.set_link('5')
        assert(media.get_message_id() == '5')
        ```
        """
        self.message_id = new_message_id
