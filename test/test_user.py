import pytest
from shared.models.user import User

def test_eq():
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

def test_to_json_none():
    user = User(
        'my_name',
        'my_first_name',
        'my_email',
        1706873888
    )
    assert(
        user.to_json() ==
        '{' \
            '"name": "my_name", ' \
            '"first_name": "my_first_name", ' \
            '"email": "my_email", ' \
            '"join_date": 1706873888' \
        '}'
    )

def test_to_json_not_none():
    user = User(
        'my_name',
        'my_first_name',
        'my_email',
        1706873888,
        id = '5',
        auth_id = '4'
    )
    assert(
        user.to_json() ==
        '{' \
            '"id": "5", ' \
            '"name": "my_name", ' \
            '"first_name": "my_first_name", ' \
            '"email": "my_email", ' \
            '"join_date": 1706873888, ' \
            '"auth_id": "4"' \
        '}'
    )

def test_str_none():
    user = User(
        'my_name',
        'my_first_name',
        'my_email',
        1706873888
    )
    assert(
        str(user) ==
        '{' \
            '"name": "my_name", ' \
            '"first_name": "my_first_name", ' \
            '"email": "my_email", ' \
            '"join_date": 1706873888' \
        '}'
    )

def test_str_not_none():
    user = User(
        'my_name',
        'my_first_name',
        'my_email',
        1706873888,
        id = '5',
        auth_id = '4'
    )
    assert(
        str(user) ==
        '{' \
            '"id": "5", ' \
            '"name": "my_name", ' \
            '"first_name": "my_first_name", ' \
            '"email": "my_email", ' \
            '"join_date": 1706873888, ' \
            '"auth_id": "4"' \
        '}'
    )

def test_from_json_none():
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

def test_from_json_not_none():
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

def test_get_name():
    user = User(
        "my_name",
        "my_first_name",
        "my_email",
        1706873888,
        id = "5",
        auth_id = "4"
    )
    assert(user.get_name() == "my_name")


def test_get_first_name():
    user = User(
        "my_name",
        "my_first_name",
        "my_email",
        1706873888,
        id = "5",
        auth_id = "4"
    )
    assert(user.get_first_name() == "my_first_name")

def test_get_email():
    user = User(
        "my_name",
        "my_first_name",
        "my_email",
        1706873888,
        id = "5",
        auth_id = "4"
    )
    assert(user.get_email() == "my_email")

def test_get_join_date():
    user = User(
        "my_name",
        "my_first_name",
        "my_email",
        1706873888,
        id = "5",
        auth_id = "4"
    )
    assert(user.get_join_date() == 1706873888)

def test_get_id_none():
    user = User(
        "my_name",
        "my_first_name",
        "my_email",
        1706873888,
    )
    assert(user.get_id() == None)

def test_get_id_not_none():
    user = User(
        "my_name",
        "my_first_name",
        "my_email",
        1706873888,
        id = "5",
        auth_id = "4"
    )
    assert(user.get_id() == '5')

def test_get_auth_id_none():
    user = User(
        "my_name",
        "my_first_name",
        "my_email",
        1706873888,
    )
    assert(user.get_auth_id() == None)

def test_get_auth_id_not_none():
    user = User(
        "my_name",
        "my_first_name",
        "my_email",
        1706873888,
        id = "5",
        auth_id = "4"
    )
    assert(user.get_auth_id() == '4')

def test_set_name():
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

def test_set_first_name():
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

def test_set_email():
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

def test_set_id():
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

def test_set_auth_id():
    user = User(
        "my_name",
        "my_first_name",
        "my_email",
        1706873888,
    )
    assert(user.get_auth_id() == None)
    user.set_auth_id('5')
    assert(user.get_auth_id() == '5')

