from flask_injector import request
from injector import Binder, singleton
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from core.models import User, Achievement
from core.services.achievement_service import AchievementService, IAchievementService
from core.services.user_service import IUserService, UserService
from dal.context import Base
from dal.repositories.achievement_repositories import AchievementRepository
from dal.repositories.repository import EntityRepository
from dal.repositories.user_repositories import UserRepository


class Config:
    PG_USER = 'postgres'
    PG_PASSWORD = 'postgres'
    PG_HOST = 'localhost'
    PG_DATABASE = 'AchievementsServiceDB'

    SWAGGER_URL = '/swagger'
    API_URL = '/swagger.json'

    connection_string = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:5432/{PG_DATABASE}"


class InjectorConfig:
    @staticmethod
    def configure(binder: Binder):
        engine = create_engine(Config.connection_string)
        Base.metadata.create_all(engine)

        session = sessionmaker(bind=engine)

        binder.bind(Engine, to=engine, scope=singleton)
        binder.bind(Session, to=session(), scope=request)

        binder.bind(EntityRepository[User], to=UserRepository, scope=request)
        binder.bind(EntityRepository[Achievement], to=AchievementRepository, scope=request)

        binder.bind(IUserService, to=UserService, scope=request)
        binder.bind(IAchievementService, to=AchievementService, scope=request)
