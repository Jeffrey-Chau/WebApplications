"""
This file defines the database models
"""
import datetime

from . common import db, Field, auth
from pydal.validators import *


def get_user_email():
     return auth.current_user.get('email')

db.define_table(
    'contact',
    Field('first_name'),
    Field('last_name'),
    Field('user_email', default=get_user_email)
)

db.contact.first_name.requires = IS_NOT_EMPTY()
db.contact.last_name.requires = IS_NOT_EMPTY()

db.contact.user_email.readable = False
db.contact.id.readable = False



db.define_table(
    'phones',
    Field('phone'),
    Field('kind'),
    Field('phone_id', 'reference contact'),
    Field('user_email', default=get_user_email)
)

db.phones.phone.requires = IS_NOT_EMPTY()
db.phones.kind.requires = IS_NOT_EMPTY()

db.phones.id.readable = False
db.phones.phone_id.readable = False
db.phones.user_email.readable = False


db.commit()