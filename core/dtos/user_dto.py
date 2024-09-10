from typing import Optional, List

from marshmallow import Schema, fields

from core.dtos.achievement_dto import AchievementDetailsSchema, AchievementDetailsDTO
from core.enums.language_code import LanguageCode


class UserSummarySchema(Schema):
    """Используется для отображения общей информации о пользователе"""
    id = fields.Int(required=True)
    username = fields.String(required=True)
    language = fields.String(required=True)

    achievements = fields.List(fields.Nested(AchievementDetailsSchema))


class UserSummaryDTO:
    """Объект dto, содержащий общую о пользователе"""

    def __init__(self, id, username, language: LanguageCode,
                 achievements: Optional[List[AchievementDetailsDTO]] = None):
        self.id = id
        self.username = username
        self.language = language.value
        self.achievements = achievements


class UserSchema(Schema):
    username = fields.String(required=True)
    language_id = fields.Integer(required=True)


class UserDTO:
    def __init__(self, username, language_id):
        self.username = username
        self.language_id = language_id
