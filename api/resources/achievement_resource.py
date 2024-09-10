import json
import logging
from http import HTTPStatus

from flasgger import swag_from
from flask import Response
from flask_restful import Resource, reqparse
from injector import inject
from marshmallow import ValidationError

from core.dtos.achievement_dto import AchievementSchema
from core.enums.language_code import LanguageCode
from core.services.achievement_service import IAchievementService


class AchievementAPI(Resource):
    """Ресурс отвечает за crud операции над достижениями"""

    @inject
    def __init__(self, service: IAchievementService):
        self._service = service

    @swag_from('../api-specs/api-specs.yml')
    def get(self) -> tuple[Response, HTTPStatus]:
        """Возвращает информацию о достижении на выбранном языке"""
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, location='args', help='Achievement id can not be blank')
        parser.add_argument('language', type=str, required=True, location='args', help='Language code can not be blank')

        args = parser.parse_args()
        id = int(args['id'])
        language = args['language'].upper()

        if language.upper() not in LanguageCode.__members__:
            logging.error(f"Error occurred while processing request: uncorrected language")
            return {'error': 'uncorrected language'}, HTTPStatus.BAD_REQUEST

        logging.info(f"Successfully returned achievement info #{id}")
        return self._service.get_details(id, LanguageCode[language])

    @swag_from('../api-specs/api-specs.yml')
    def post(self) -> HTTPStatus:
        """Добавляет достижение с его описаниями на разных языках"""
        schema = AchievementSchema()
        parser = reqparse.RequestParser()
        parser.add_argument('achievement', type=str, help="Achievement data required!")

        args = parser.parse_args()

        try:
            achievement_data = json.loads(args['achievement'].replace("'", "\""))
            validated_data = schema.load(achievement_data)

        except ValidationError:
            logging.error("Error occurred while processing the request: achievement data is uncorrected")
            return {'error': 'achievement data is uncorrected'}, HTTPStatus.BAD_REQUEST

        self._service.add(validated_data)
        logging.info("Successfully added achievement")
        return HTTPStatus.OK

    @swag_from('../api-specs/api-specs.yml')
    def put(self) -> HTTPStatus:
        """Обновляет информации о достижении, включая описания"""
        schema = AchievementSchema()
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, location='args')
        parser.add_argument('achievement', type=str, help="Achievement data required!")

        args = parser.parse_args()

        try:
            achievement_data = json.loads(args['achievement'].replace("'", "\""))
            validated_data = schema.load(achievement_data)

        except ValidationError:
            logging.error("Error occurred while processing the request: achievement data is uncorrected")
            return {'error': 'achievement data is uncorrected'}, HTTPStatus.BAD_REQUEST

        validated_data["id"] = int(args['id'])

        self._service.update(validated_data)
        logging.info("Successfully updated achievement")
        return HTTPStatus.OK

    @swag_from('../api-specs/api-specs.yml')
    def delete(self) -> HTTPStatus:
        """Удаляет достижение вместе с описаниями"""
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, location='args')

        args = parser.parse_args()

        self._service.delete(int(args['id']))
        return HTTPStatus.OK
