from peewee import Model, CharField, ForeignKeyField, IntegerField, TimeField
from database.database import db

class Videos(Model):
    nome_video = CharField()
    qtde_comentarios = IntegerField()
    url = CharField()

    class Meta:
        database = db
