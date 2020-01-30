from models.base_model import BaseModel
from playhouse.hybrid import hybrid_property
from models.user import User
import peewee as pw


class Donation(BaseModel):
    amount = pw.DecimalField(decimal_places=2)
    user = pw.ForeignKeyField(User, null=True, backref="donations")
    