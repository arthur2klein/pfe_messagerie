import pytest
from shared.models.group import Group
from shared.models.user import User

def test_get_id_none():
    group_name = 'my_group'
    new_group1 = Group(group_name)
    assert(new_group1.get_id() == None)

def test_get_id_not_none():
    group_name = 'my_group'
    new_group2 = Group(group_name, id = '5')
    assert(new_group2.get_id() == '5')

def test_get_name():
    group_name = 'my_group'
    new_group = Group(group_name)
    assert(new_group.get_name() == group_name)

def test_set_id():
    group_name = 'my_group'
    new_group = Group(group_name)
    assert(new_group.get_id() == None)
    new_group.set_id('5')
    assert(new_group.get_id() == '5')

def test_set_name():
    group_name = 'my_group'
    new_group = Group(group_name)
    assert(new_group.get_name() == group_name)
    new_name = 'my_group_'
    new_group.set_name(new_name)
    assert(new_group.get_name() == group_name)

def test_to_json_id_none():
    group_name = 'my_group'
    new_group1 = Group(group_name)
    json_group1 = new_group1.to_json()
    assert(json_group1 == '{"name": "my_group"}')

def test_to_json_id_not_none():
    group_name = 'my_group'
    new_group2 = Group(group_name, id = '5')
    json_group2 = new_group2.to_json()
    assert(json_group2 == '{"id": "5", "name": "my_group"}')

def test_str_id_none():
    group_name = 'my_group'
    new_group1 = Group(group_name)
    json_group1 = str(new_group1)
    assert(json_group1 == '{"name": "my_group"}')

def test_str_id_not_none():
    group_name = 'my_group'
    new_group2 = Group(group_name, id = '5')
    json_group2 = str(new_group2)
    assert(json_group2 == '{"id": "5", "name": "my_group"}')

def test_eq_equals():
    group1 = Group('my_group', 'id')
    group2 = Group('my_group', 'id')
    assert(group1 == group2)

def test_eq_different_id():
    group1 = Group('my_group', 'id')
    group2 = Group('my_group')
    assert(group1 != group2)

def test_eq_different_name():
    group1 = Group('my_group', 'id')
    group2 = Group('group', 'id')
    assert(group1 != group2)

def test_from_json_id_none():
    json_string = '{"name": "my_group"}'
    new_group = Group.from_json(json_string)
    assert(new_group == Group('my_group'))

def test_from_json_id_not_none():
    json_string = '{"id": "5", "name": "my_group"}'
    new_group = Group.from_json(json_string)
    assert(new_group == Group('my_group', id = '5'))

def test_get_users():
    user = User('name', 'first_name', 'email', 0)
    group = Group('my_group', l_users = [user])
    assert(list(group.get_users()) == [user])

def test_set_users():
    user = User('name', 'first_name', 'email', 0)
    group = Group('my_group')
    assert(list(group.get_users()) == [])
    group.set_users([user])
    assert(list(group.get_users()) == [user])

def test_add_user():
    user = User('name', 'first_name', 'email', 0)
    group = Group('my_group')
    assert(list(group.get_users()) == [])
    group.add_user(user)
    assert(list(group.get_users()) == [user])

def test_remove_user():
    user = User('name', 'first_name', 'email', 0)
    group = Group('my_group', l_users = [user])
    assert(list(group.get_users()) == [user])
    assert(group.remove_user(user))
    assert(list(group.get_users()) == [])
    assert(not(group.remove_user(user)))

def test_contains_user():
    user = User('name', 'first_name', 'email', 0)
    group = Group('my_group', l_users = [user])
    assert(list(group.get_users()) == [user])
    assert(group.remove_user(user))
    assert(list(group.get_users()) == [])
    assert(not(group.remove_user(user)))

