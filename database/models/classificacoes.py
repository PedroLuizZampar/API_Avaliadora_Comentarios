from peewee import Model, ForeignKeyField, CharField
from database.database import db
from database.models.comentarios import Comentarios

class Classificacoes(Model):
    comentario = ForeignKeyField(Comentarios, backref='comentarios', on_delete='CASCADE', null=True)
    classificacao = CharField()

    class Meta:
        database = db
