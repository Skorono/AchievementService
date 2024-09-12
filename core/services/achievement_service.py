from abc import abstractmethod
from typing import Optional, List

from injector import inject

from core.dtos.achievement_dto import AchievementDetailsSchema, AchievementSchema
from core.enums.language_code import LanguageCode
from core.helpers.dto_transformer import DtoTransformer
from core.helpers.model_transformer import ModelTransformer
from core.models import Achievement
from core.services.service import Service, T
from dal.repositories.repository import EntityRepository


class IAchievementService(Service[Achievement]):
    @inject
    def __init__(self, repository: EntityRepository[Achievement]):
        super().__init__(repository)

    @abstractmethod
    def get_details(self, id: int, lang_code: str) -> Optional[AchievementDetailsSchema]:
        """Возвращает dto достижения с подробной информацией о ней на выбранном языке"""
        pass


class AchievementService(IAchievementService):

    @inject
    def __init__(self, repository: EntityRepository[Achievement]):
        super().__init__(repository)

    def get(self, id: int) -> Optional[AchievementSchema]:
        achievement = super().get(id)

        if achievement is None:
            return None

        return AchievementSchema().dump(achievement)
    
    def get_all(self) -> List[AchievementSchema]:
        achievements = self._get_all()
        return AchievementSchema().dump(achievements, many=True)

    def update(self, achievement_dto: AchievementSchema):
        achievement = ModelTransformer.achievement_to_model(achievement_dto)
        super().update(achievement)

    def add(self, achievement_dto: AchievementSchema):
        achievement = ModelTransformer.achievement_to_model(achievement_dto)
        super().add(achievement)

    def get_details(self, id: int, lang_code: LanguageCode):
        schema = AchievementDetailsSchema()
        achievement = super().get(id)

        achievements_dto = DtoTransformer.achievement_to_dto(achievement, LanguageCode[lang_code.value])

        return schema.dump(achievements_dto)
