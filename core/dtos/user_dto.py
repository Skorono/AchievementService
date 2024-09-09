from typing import Optional, List

from marshmallow import Schema, fields

from core.dtos.achievement_dto import AchievementDetailsSchema, AchievementDetailsDTO
from core.enums.language_code import LanguageCode


class UserSummarySchema(Schema):
    id = fields.Int(required=True)
    username = fields.String(required=True)
    language = fields.String(required=True)

    achievements = fields.List(fields.Nested(AchievementDetailsSchema))


class UserSummaryDTO:
    def __init__(self, id, username, language: LanguageCode, achievements: Optional[List[AchievementDetailsDTO]]):
        self.id = id
        self.username = username
        self.language = language.value
        self.achievements = achievements
