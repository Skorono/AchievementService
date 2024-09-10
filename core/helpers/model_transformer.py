from core.dtos.achievement_dto import AchievementSchema
from core.dtos.user_dto import UserSchema, UserSummarySchema
from core.models import Achievement, User, AchievementDescription


class ModelTransformer:
    """Преобразует dto модели к моделям базы данных"""

    @staticmethod
    def user_to_model(self, user_dto: UserSchema) -> User:
        pass

    @staticmethod
    def user_summary_to_model(user_dto: UserSummarySchema) -> User:
        pass

    @staticmethod
    def achievement_to_model(achievement_dto: AchievementSchema) -> Achievement:
        achievement = Achievement()
        descriptions = list()
        for description_dto in achievement_dto["descriptions"]:
            description = AchievementDescription()
            description.text = description_dto["text"]
            description.language_id = description_dto["language_id"]
            description.name = description_dto["name"]

            descriptions.append(description)

        achievement.scores = achievement["scores"]
        achievement.descriptions = descriptions

        return achievement

    @staticmethod
    def achievement_summary_to_model(achievement_dto: AchievementSchema) -> Achievement:
        pass
