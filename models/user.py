from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    name = pw.CharField(unique=False)
    password = pw.CharField(unique=False)
    username = pw.CharField(unique=True)

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_name = User.get_or_none(User.name == self.name)

        if duplicate_name:
            self.errors.append('Name has been taken')

        if duplicate_username:
            self.errors.append('Username has been taken')
