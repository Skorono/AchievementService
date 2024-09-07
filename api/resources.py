from http import HTTPStatus
from typing import List

from flask_apispec import marshal_with, MethodResource, doc
from injector import inject

from core.models import User
from core.schemes import UserSchema
from core.services import UserServiceBase


class UserResource(MethodResource):
    @inject
    def __init__(self, service: UserServiceBase):
        self._service = service
        self._user_schema = UserSchema()
        self._users_schema = UserSchema(many=True)

    @doc(responses={200: {'description': 'Users returned'}})
    @marshal_with(UserSchema)
    def get(self, user_id: int = None) -> tuple[List[User], HTTPStatus]:
        if user_id:
            return self._user_schema.dump(self._service.get(user_id)), HTTPStatus.OK
        else:
            users = self._service.get_all()
            return self._users_schema.dump(users), HTTPStatus.OK

    def post(self) -> None:
        pass

# class AchievementResource(ResourceBase[Achievement]):
#    pass
