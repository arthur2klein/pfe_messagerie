import pytest
from shared.models.message import Message

def test_eq():
    message1 = Message(
            content = 'Hello world!',
            sender_id = '1',
            receiver_group_id = '2',
            date = 1706873888
            )
    message2 = Message(
            content = 'Hello world!',
            sender_id = '1',
            receiver_group_id = '2',
            date = 1706873888
            )
    message3 = Message(
            content = 'Hello world!',
            sender_id = '1',
            receiver_group_id = '2',
            date = 1706873898
            )
    assert(message1 == message2)
    assert(message1 != message3)

def test_from_json():
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

def test_to_json():
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

def test_to_json_id():
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
    message_json = message.to_json()
    assert(message_json == target)

def test_str():
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

def test_get_content():
    message = Message(
            content = 'Hello world!',
            sender_id = '1',
            receiver_group_id = '2',
            date = 1706873888,
            id = '4'
            )
    assert(message.get_content() == 'Hello world!')

def test_get_sender_id():
    message = Message(
            content = 'Hello world!',
            sender_id = '1',
            receiver_group_id = '2',
            date = 1706873888,
            id = '4'
            )
    assert(message.get_sender_id() == '1')

def test_get_receiver_group_id():
    message = Message(
            content = 'Hello world!',
            sender_id = '1',
            receiver_group_id = '2',
            date = 1706873888,
            id = '4'
            )
    assert(message.get_receiver_group_id() == '2')

def test_get_date():
    message = Message(
            content = 'Hello world!',
            sender_id = '1',
            receiver_group_id = '2',
            date = 1706873888,
            id = '4'
            )
    assert(message.get_date() == 1706873888)

def test_get_id():
    message = Message(
            content = 'Hello world!',
            sender_id = '1',
            receiver_group_id = '2',
            date = 1706873888,
            id = '4'
            )
    assert(message.get_id() == '4')

def test_set_content():
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

def test_set_sender_id():
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

def test_set_receiver_group_id():
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

def test_set_date():
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

def test_set_id():
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

