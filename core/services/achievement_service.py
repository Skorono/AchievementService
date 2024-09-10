from abc import abstractmethod
from typing import Optional, List

from injector import inject

from core.dtos.achievement_dto import AchievementDetailsSchema, AchievementDTO, AchievementSchema
from core.enums.language_code import LanguageCode
from core.helpers.dto_transformer import DtoTransformer
from core.helpers.model_transformer import ModelTransformer
from core.models import Achievement, AchievementDescription
from core.services.service import Service
from dal.repositories.repository import EntityRepository


class IAchievementService(Service[Achievement]):
    @inject
    def __init__(self, repository: EntityRepository[Achievement]):
        super().__init__(repository)

    @abstractmethod
    def get_details(self, id: int, lang_code: str) -> Optional[AchievementDetailsSchema]:
        pass


class AchievementService(IAchievementService):
    @inject
    def __init__(self, repository: EntityRepository[Achievement]):
        super().__init__(repository)

    def update(self, achievement_dto: AchievementSchema):
        achievement = ModelTransformer.achievement_to_model(achievement_dto)
        super().update(achievement)

    def add(self, achievement_dto: AchievementDTO):
        achievement = Achievement()
        achievement_descriptions: List[AchievementDescription] = list()

        # Todo: преобразования должны находится не здесь но пока оставлю так
        for description_dto in achievement_dto.descriptions:
            description = AchievementDescription()
            description.text = description_dto.text
            description.name = description_dto.name
            description.language_id = description_dto.language_id
            achievement_descriptions.append(description)

        achievement.scores = achievement_dto.scores
        achievement.descriptions = achievement_descriptions

        super().add(achievement)

    def get_details(self, id: int, lang_code: LanguageCode):
        schema = AchievementDetailsSchema()
        achievement = self.get(id)

        achievements_dto = DtoTransformer.achievement_to_dto(achievement, LanguageCode[lang_code.value])

        return schema.dump(achievements_dto)
