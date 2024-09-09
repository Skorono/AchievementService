from http import HTTPStatus

from flasgger import swag_from
from flask import jsonify, Response
from flask_restful import reqparse, Resource
from injector import inject

from core.services.user_service import IUserService

user_schema = {
    'type': 'object',
    'properties': {
        'id': {
            'type': 'integer',
            'description': 'User ID',
            'example': 1
        },
        'username': {
            'type': 'string',
            'description': 'User name',
            'example': 'John Doe'
        },
    },
    'required': ['id', 'username']
}


class UserAPI(Resource):
    @inject
    def __init__(self, service: IUserService):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user')

        self._service = service

    @swag_from({
        'parameters': [
            {
                'name': 'user_id',
                'description': 'ID of the user',
                'in': 'path',
                'type': 'integer',
                'required': True
            }
        ],
        'responses': {
            200: {
                'description': 'User returned',
                'schema': user_schema
            },
            404: {
                'description': 'User not found'
            }
        },
    })
    def get(self, user_id: int) -> tuple[Response, HTTPStatus]:
        user = self._service.get(user_id)
        if user is None:
            return jsonify({'error': 'user not found'}), HTTPStatus.NOT_FOUND

        return self._user_schema.dump(user), HTTPStatus.OK

    @swag_from({
        'parameters': [
            {
                'name': 'user',
                'in': 'body',
                'required': True,
                'schema': user_schema
            }
        ],
        'responses': {
            201: {
                'description': 'User created',
                'schema': user_schema
            },
            400: {
                'description': 'Cannot parse arguments'
            }
        }
    })
    def post(self) -> tuple[Response, HTTPStatus]:
        args = self.parser.parse_args()

        user_data = self._user_schema.load(args['user'])
        if user_data is None:
            return jsonify({'error': 'cannot parse arguments'}), HTTPStatus.BAD_REQUEST

        self._service.add(user_data)
        return user_data, HTTPStatus.CREATED

    def delete(self, user_id: int) -> HTTPStatus:
        self._service.delete(user_id)
        return HTTPStatus.OK

    # def put(self):
    #     args = self.parser.parse_args()
    #
    #     user_data = self._user_schema.load(args['user'])
    #     if user_data is None:
    #         return jsonify({'error': 'cannot parse arguments'}), HTTPStatus.BAD_REQUEST
    #
    #     user = self._service.get(user_data.id)


class UsersAPI(Resource):
    def __init__(self, service: IUserService):
        self._service = service

    def get(self) -> tuple[Response, HTTPStatus]:
        users = self._service.get_all()
        return self._schema.dump(users), HTTPStatus.OK


class UserAchievementsAPI(Resource):
    def __init__(self, service: IUserService):
        self._service = service

    def get(self, user_id: int) -> tuple[Response, HTTPStatus]:
        achievements = self._service.get_achievements(user_id)
        return achievements, HTTPStatus.OK


class UserStatisticScoreLeaderAPI(Resource):
    def __init__(self, service: IUserService):
        self._service = service

    def get(self) -> tuple[Response, HTTPStatus]:
        return self._service.get_score_leader(), HTTPStatus.OK
