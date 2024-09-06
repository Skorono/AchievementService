from flask import Flask
from flask_injector import FlaskInjector, request
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from injector import Binder, singleton
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from api.config import Config
from api.resources import UserResource
from core.models import Base, User, Achievement
from core.services import UserService, AchievementService, Service
from dal.repositories import UserRepository, AchievementRepository, EntityRepository

app = Flask(__name__)
api = Api(app)

ma = Marshmallow(app)

swaggerui_blueprint = get_swaggerui_blueprint(
    Config.SWAGGER_URL,
    Config.API_URL,
    config={
        'app_name': "Achievement Service API"
    }
)


def configure(binder: Binder):
    engine = create_engine(Config.connection_string)
    Base.metadata.create_all(engine)

    session = sessionmaker(bind=engine)

    binder.bind(Engine, to=engine, scope=singleton)
    binder.bind(Session, to=session(), scope=request)

    binder.bind(EntityRepository[User], to=UserRepository, scope=request)
    binder.bind(EntityRepository[Achievement], to=AchievementRepository, scope=request)

    binder.bind(Service[User], to=UserService, scope=request)
    binder.bind(Service[Achievement], to=AchievementService, scope=request)


injector = FlaskInjector(app=app, modules=[configure])

api.add_resource(UserResource, '/users', '/users/<int:user_id>',
                 resource_class_kwargs={'service': injector.injector.get(UserService)})
# api.add_resource(injector.injector.get(AchievementResource), '/achievements/<int:achievement_id>')

app.register_blueprint(swaggerui_blueprint, url_prefix=Config.SWAGGER_URL)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
