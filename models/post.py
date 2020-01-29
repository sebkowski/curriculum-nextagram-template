from models.base_model import BaseModel
from models.user import User
import peewee as pw




class Post(BaseModel):
    user= pw.ForeignKeyField(User, backref ='posts')
    image_path=pw.CharField()
    caption=pw.CharField(null=True)
    
    