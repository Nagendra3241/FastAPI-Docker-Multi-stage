from tortoise.models import Model
from tortoise.fields import IntField, DatetimeField, ForeignKeyField, ManyToManyField, DecimalField, CharField, BigIntField

class User(Model):
    class Meta:
        table = "users"

    id              = IntField(pk=True)
    email           = CharField(max_length=255)
    name            = CharField(max_length=255) 
    id_token        = CharField(max_length=2048) 
    access_token    = CharField(max_length=255)
    refresh_token   = CharField(max_length=255)
    picture         = CharField(max_length=255)
    locale          = CharField(max_length=255)
    created_at      = DatetimeField(auto_now_add=True)
    update_at       = DatetimeField(auto_now=True)

    def __str__(self):
        return self.name