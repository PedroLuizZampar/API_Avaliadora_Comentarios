from peewee import Model, CharField, ForeignKeyField, BooleanField
from database.database import db
from database.models.videos import Videos

class Comentarios(Model):
    video = ForeignKeyField(Videos, backref='videos', on_delete='CASCADE', null=True)
    comentario = CharField()
    classificado = BooleanField(default=False)

    class Meta:
        database = db
