from marshmallow import Schema, fields


class AchievementDetailsSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    scores = fields.Int(required=True)
    text = fields.String(required=True)


class AchievementDetailsDTO:
    def __init__(self, id, name, scores, text):
        self.id = id
        self.name = name
        self.scores = scores
        self.text = text
