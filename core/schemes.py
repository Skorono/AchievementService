from flask_marshmallow.sqla import SQLAlchemyAutoSchema

from core.models import User, Achievement


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True


class AchievementSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Achievement
        load_instance = True
