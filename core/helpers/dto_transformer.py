from typing import List

from core.dtos.achievement_dto import AchievementDetailsDTO
from core.dtos.user_dto import UserSummaryDTO
from core.enums.language_code import LanguageCode
from core.models import Achievement, User


class DtoTransformer:
    """Преобразует модели базы данных в dto"""
    @staticmethod
    def achievement_to_dto(achievement: Achievement, language: LanguageCode) -> AchievementDetailsDTO:
        achievement_dto: AchievementDetailsDTO = None

        for achievement_description in achievement.descriptions:
            if achievement_description.language.code == language.value:
                achievement_dto = AchievementDetailsDTO(
                    id=achievement.id,
                    name=achievement_description.name,
                    scores=achievement.scores,
                    text=achievement_description.text
                )

        return achievement_dto

    @staticmethod
    def achievements_to_dto(achievements: List[Achievement], language: LanguageCode) -> List[AchievementDetailsDTO]:
        achievements_dtos = list()

        for achievement in achievements:
            achievements_dtos.append(DtoTransformer.achievement_to_dto(achievement, language))

        return achievements_dtos

    @staticmethod
    def user_to_dto(user: User) -> UserSummaryDTO:
        user_dto = UserSummaryDTO(
            id=user.id,
            username=user.username,
            language=LanguageCode[user.language.code],
            achievements=DtoTransformer.achievements_to_dto(user.achievements,
                                                            language=LanguageCode[user.language.code])
        )

        return user_dto
