from models.base_model import BaseModel
from werkzeug.security import generate_password_hash
from flask_login import UserMixin, current_user
from playhouse.hybrid import hybrid_property
import peewee as pw
import re 



class User(UserMixin, BaseModel):
    name = pw.CharField(unique=False)
    password = pw.CharField(unique=False)
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True )
    profile_image = pw.CharField(unique=False, default='http://sebagram.s3.amazonaws.com/user.png') 
    private = pw.BooleanField(default=False)

    @hybrid_property
    def followers(self):
        return [x.follower for x in self.follower]
    
    @hybrid_property
    def sum_followers(self):
        return len(self.followers)
    
    @hybrid_property
    def followings(self):
        return [x.following for x in self.following]
    
    @hybrid_property
    def sum_followings(self):
        return len(self.followings)
    
    @hybrid_property
    def pending_requests(self):
        from models.followers import Followstate
        query = Followstate.select().where(Followstate.following_id == self.id, Followstate.approved == False)
        return [x.follower for x in query]

    @hybrid_property
    def sum_pending_request(self):
        return len(self.pending_requests)
    

    
    # @hybrid_property
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
            # this is an update, not create
            if self.id:
                self.password = self.password
            else:
                self.password=generate_password_hash(self.password)
