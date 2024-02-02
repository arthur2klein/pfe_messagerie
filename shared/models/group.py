from __future__ import annotations
from typing import Type
import json

class Group:
  """ Represents a group of people able to discuss with each other.
  ---
  Attributes:
    id (Optional[str]): Id of the group in the database.
    name (str): Name of the group.
  ---
  Methods:
    __eq__(Self, Self) -> bool: Check for equality between two groups.
    __init__(Self, str, Optional[str]): Create a new group.
    __repr__(Self) -> str: Convert the instance to a displayable string
    __str__(Self) -> str: Convert the instance to a string
    from_json(str) -> Self: Convert a json string to a new goup
    get_id(Self) -> Optional[str]: Returns the id of the current group
    get_name(Self) -> str: Returns the name of the current group
    get_id(Self, Optional[str]): Modify the id of the current group
    get_name(Self, str): Modify the name of the current group
    to_json(Self) -> str: Convert a group to a json string
  """

  def __init__(
    self: Self,
    name: str,
    id: Optional[str] = None
  ):
    """ Returns a discussion group.
    id will generally be set by the database.
    ---
    Parameters:
      self (Self): Current instance.
      name (str): Name of the new group.
      id (Optional[str]): Id of the new group, generally set by the
      database.
    ---
    Example:
    ```python
    group_name = 'my_group'
    new_group = Group(group_name)
    """
    self.id = id
    self.name = name

  def __eq__(self: Self, other: Self) -> bool:
    """ Check for equality between two instances.
    ---
    Parameters:
      self (Self): Current instance.
      other (Self): Instance to compare to.
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
    Paramters:
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
      return f'{{"name": "{self.name}"}}'
    else:
      return f'{{"id": "{self.id}", "name": "{self.name}"}}'

  def __repr__(self: Self) -> str:
    """ Convert the current instance to a json string.
    The id field is absent if None.
    ---
    Paramters:
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
    return self.to_json()

  def __str__(self: Self) -> str:
    """ Convert the current instance to a json string.
    The id field is absent if None.
    ---
    Paramters:
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
