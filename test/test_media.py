import pytest
from shared.models.media import Media

def test_eq():
    media1 = Media('mon_image', 'img', 'link/to/image.png', '3')
    media2 = Media('mon_image', 'img', 'link/to/image.png', '3')
    media3 = Media('mon_image', 'img', 'link/to/img.png', '3')
    assert(media1 == media2)
    assert(media1 != media3)

def test_from_json_id_none():
    target = Media('mon_image', 'img', 'link/to/image.png', '3')
    media_json = '{ ' \
            '"name": "mon_image", ' \
            '"type_": "img", ' \
            '"link": "link/to/image.png", ' \
            '"message_id": "3"}'
    media = Media.from_json(media_json)
    assert(media == target)

def test_from_json_id_not_none():
    target = Media('mon_image', 'img', 'link/to/image.png', '3', id = '4')
    media_json = '{ ' \
            '"name": "mon_image", ' \
            '"type_": "img", ' \
            '"link": "link/to/image.png", ' \
            '"message_id": "3", ' \
            '"id": "4"}'
    media = Media.from_json(media_json)
    assert(media == target)

def test_str():
    media = Media('mon_image', 'img', 'link/to/image.png', '3', id = '4')
    target = '{"id": "4", ' \
            '"name": "mon_image", ' \
            '"type_": "img", ' \
            '"link": "link/to/image.png", ' \
            '"message_id": "3"}'
    media_json = str(media)
    assert(media_json == target)

def test_to_json():
    media = Media('mon_image', 'img', 'link/to/image.png', '3', id = '4')
    target = '{"id": "4", ' \
            '"name": "mon_image", ' \
            '"type_": "img", ' \
            '"link": "link/to/image.png", ' \
            '"message_id": "3"}'
    media_json = media.to_json()
    assert(media_json == target)
    
def test_get_id_none():
    media = Media('mon_image', 'img', 'link/to/image.png', '3')
    assert(media.get_id() == None) 

def test_get_id_not_none():
    media = Media('mon_image', 'img', 'link/to/image.png', '3', id = '4')
    assert(media.get_id() == '4')

def test_get_name():
    media = Media('mon_image', 'img', 'link/to/image.png', '3', id = '4')
    assert(media.get_name() == 'mon_image')

def test_get_type():
    media = Media('mon_image', 'img', 'link/to/image.png', '3', id = '4')
    assert(media.get_type() == 'img')

def test_get_link():
    media = Media('mon_image', 'img', 'link/to/image.png', '3', id = '4')
    assert(media.get_link() == 'link/to/image.png')

def test_get_message_id():
    media = Media('mon_image', 'img', 'link/to/image.png', '3', id = '4')
    assert(media.get_message_id() == '3')

def test_set_id():
    media = Media('mon_image', 'img', 'link/to/image.png', '3')
    assert(media.get_id() == None)
    media.set_id('4')
    assert(media.get_id() == '4')

def test_set_name():
    media = Media('mon_image', 'img', 'link/to/image.png', '3')
    assert(media.get_name() == 'mon_image')
    media.set_name('new_name')
    assert(media.get_name() == 'new_name')

def test_set_type():
    media = Media('mon_image', 'img', 'link/to/image.png', '3')
    assert(media.get_type() == 'img')
    media.set_type('audio')
    assert(media.get_type() == 'audio')

def test_set_link():
    media = Media('mon_image', 'img', 'link/to/image.png', '3')
    assert(media.get_link() == 'link/to/image.png')
    media.set_link('link/to/img.png')
    assert(media.get_link() == 'link/to/img.png')

def test_set_message_id():
    media = Media('mon_image', 'img', 'link/to/image.png', '3')
    assert(media.get_message_id() == '3')
    media.set_message_id('5')
    assert(media.get_message_id() == '5')

