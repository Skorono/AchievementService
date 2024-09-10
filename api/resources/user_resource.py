import json
import logging
from http import HTTPStatus

from flasgger import swag_from
from flask import jsonify, Response
from flask_restful import reqparse, Resource
from injector import inject
from marshmallow import ValidationError

from core.dtos.user_dto import UserSchema
from core.models import User
from core.services.user_service import IUserService


class UserAPI(Resource):
    @inject
    def __init__(self, service: IUserService):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user')

        self._service = service

    @swag_from('../api-specs/api-specs.yml', endpoint='user.get')
    def get(self) -> tuple[Response, HTTPStatus]:
        schema = UserSchema()
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, location='args')

        args = parser.parse_args()

        user = self._service.get(args['id'])
        if user is None:
            logging.error("Error has occurred while processing the request: there is no such user")
            return {'error': 'user not found'}, HTTPStatus.NOT_FOUND

        logging.info(f"Successfully returned user #{user.id}")
        return schema.dump(user), HTTPStatus.OK

    @swag_from('../api-specs/api-specs.yml')
    def post(self) -> tuple[Response, HTTPStatus]:
        schema = UserSchema()
        parser = reqparse.RequestParser()
        parser.add_argument('user', type=str, required=True)

        args = parser.parse_args()

        try:
            user_json = json.loads(args['user'].replace("'", "\""))
            validated_user = schema.dump(user_json)

        except ValidationError:
            logging.error("Error occurred while processing request: bad user data ")
            return jsonify({'error': 'user data is uncorrected'}), HTTPStatus.BAD_REQUEST

        user = User()
        user.username = validated_user["username"]
        user.language_id = int(validated_user["language_id"])
        self._service.add(user)

    @swag_from('../api-specs/api-specs.yml')
    def delete(self) -> HTTPStatus:
        parser = reqparse.RequestParser()
        parser.add_argument('user', type=str, required=True)
        args = parser.parse_args()

        user_id = int(args['id'])

        self._service.delete(user_id)
        logging.info(f"Successfully delete user #{user_id}")
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

    @swag_from('../api-specs/api-specs.yml')
    def get(self) -> tuple[Response, HTTPStatus]:
        schema = UserSchema()
        users = self._service.get_all()
        logging.info(f"Successfully returned users")

        return schema.dump(users, many=True), HTTPStatus.OK


class UserAchievementsAPI(Resource):
    def __init__(self, service: IUserService):
        self._service = service

    @swag_from('../api-specs/api-specs.yml')
    def get(self) -> tuple[Response, HTTPStatus]:
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, location='args')

        args = parser.parse_args()

        achievements = self._service.get_achievements(int(args['id']))
        logging.info(f"Successfully returned users achievements")

        return achievements, HTTPStatus.OK


class UserStatisticScoreLeaderAPI(Resource):
    @inject
    def __init__(self, service: IUserService):
        self._service = service

    @swag_from('../api-specs/api-specs.yml')
    def get(self) -> tuple[Response, HTTPStatus]:
        logging.info("Successfully returned score leader")
        return self._service.get_score_leader(), HTTPStatus.OK


class UserStatisticAchievementLeaderAPI(Resource):
    @inject
    def __init__(self, service: IUserService):
        self._service = service

    @swag_from('../api-specs/api-specs.yml')
    def get(self) -> tuple[Response, HTTPStatus]:
        logging.info("Successfully returned achievement leader")
        return self._service.get_achievements_leader(), HTTPStatus.OK
