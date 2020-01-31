from models.base_model import BaseModel
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property
import peewee as pw
import re 



class User(UserMixin, BaseModel):
    name = pw.CharField(unique=False)
    password = pw.CharField(unique=False)
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True )
    profile_image = pw.CharField(unique=False, default='http://sebagram.s3.amazonaws.com/user.png') 

    @hybrid_property
    def followers(self):
        return (follower.user for follower in self.followers)


    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_name = User.get_or_none(User.name == self.name)

        if duplicate_name:
            self.errors.append('Name has been taken')

        if duplicate_username:
            self.errors.append('Username has been taken')

        if len(self.password) < 6 :
            self.errors.append('Password has to be at least 6 characters')

        # pattern= '[A-Z]+[a-z]+$'
        # if re.search(pattern, self.password) is None:
        #     self.errors.append('Password must have 1 of each upper, lower and special charatcer')
        email_pattern= r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if re.search(email_pattern, self.email) is None:
            self.errors.append('Please enter a valid email')
        else: 
            self.password=generate_password_hash(self.password)
