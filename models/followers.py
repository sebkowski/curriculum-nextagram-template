from models.base_model import BaseModel
from models.user import User
from flask_login import UserMixin
import peewee as pw
import re 



class Followstate(UserMixin, BaseModel):

    following = pw.ForeignKeyField(User,  backref='follower')
    follower = pw.ForeignKeyField(User, backref='following')
    
    
