from typing import List

from marshmallow import Schema, fields, INCLUDE


class AchievementDetailsSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    scores = fields.Int(required=True)
    text = fields.String(required=True)
    issued_at = fields.DateTime(missing=None)

    class Meta:
        unknown = INCLUDE

    # Идея в том, чтобы отдавать дату выдачи достижения в случае, если оно присутствует в схеме
    # Таким образом можно не плодить новые схемы для dto достижений пользователя
    def dump(self, obj, *args, **kwargs):
        data = super().dump(obj, *args, **kwargs)

        # Проверяем, является ли data списком
        if isinstance(data, list):
            # Проходим по каждому элементу списка
            for item in data:
                if not item.get('issued_at'):
                    item.pop('issued_at', None)  # Удаляем поле, если оно отсутствует
        else:
            # Если это не список, проверяем один объект
            if not data.get('issued_at'):
                del data['issued_at']

        return data


class AchievementDetailsDTO:
    def __init__(self, id, name, scores, text, issued_at=None):
        self.id = id
        self.name = name
        self.scores = scores
        self.text = text
        self.issued_at = issued_at


class AchievementDescriptionSchema(Schema):
    name = fields.String()
    text = fields.String()
    language_id = fields.Integer()


class AchievementDescriptionDTO:
    def __init__(self, name, text, language_id):
        self.name = name
        self.text = text
        self.language_id = language_id


class AchievementSchema(Schema):
    id = fields.Integer(default=0)
    scores = fields.Integer(required=True)
    descriptions = fields.List(fields.Nested(AchievementDescriptionSchema))


class AchievementDTO:
    def __init__(self, id=0, scores=0, descriptions: List[AchievementDescriptionDTO] = None):
        self.id = id
        self.scores = scores
        self.descriptions = descriptions
