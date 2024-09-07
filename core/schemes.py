from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields

from core.models import User, Achievement


class AchievementSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Achievement
        load_instance = True


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

    achievements = fields.List(fields.Nested(AchievementSchema))
