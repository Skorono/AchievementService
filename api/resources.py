import abc
from http import HTTPStatus
from typing import TypeVar, Generic, List

from flask_apispec import marshal_with
from flask_restful import Resource
from injector import inject

from core.models import User, Achievement
from core.schemes import UserSchema
from core.services import Service

T = TypeVar("T")


class ResourceBase(abc.ABC, Generic[T], Resource):
    def __init__(self, service: Service[T]):
        self._service = service


class UserResource(ResourceBase[User]):
    @inject
    def __init__(self, service: Service[User]):
        super().__init__(service)
        self._user_schema = UserSchema()
        self._users_schema = UserSchema(many=True)

    @marshal_with(UserSchema)
    def get(self, user_id: int = None) -> tuple[List[User], HTTPStatus]:
        if user_id:
            return self._user_schema.dump(self._service.get(user_id)), HTTPStatus.OK
        else:
            users = self._service.get_all()
            return self._users_schema.dump(users), HTTPStatus.OK

    def post(self) -> None:
        pass


class AchievementResource(ResourceBase[Achievement]):
    pass
