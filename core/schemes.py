from marshmallow import Schema

from core.models import User, Achievement


class UserSchema(Schema):
    class Meta:
        model = User


class AchievementSchema(Schema):
    class Meta:
        model = Achievement
