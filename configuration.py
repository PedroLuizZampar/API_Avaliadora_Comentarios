from database.database import db
from database.models.videos import Videos
from database.models.comentarios import Comentarios
from database.models.classificacoes import Classificacoes
from routes.video import video_route

def configure_all(app):
    configure_routes(app)
    configure_db()

def configure_routes(app):
    app.register_blueprint(video_route, url_prefix = "/videos")

def configure_db():
    db.connect()
    db.create_tables([Videos])
    db.create_tables([Comentarios])
    db.create_tables([Classificacoes])