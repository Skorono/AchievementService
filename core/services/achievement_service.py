from abc import abstractmethod
from typing import Optional

from injector import inject

from core.dtos.achievement_dto import AchievementDetailsDTO, AchievementDetailsSchema
from core.enums.language_code import LanguageCode
from core.models import Achievement
from core.services.service import Service
from dal.repositories.repository import EntityRepository


class IAchievementService(Service[Achievement]):
    @inject
    def __init__(self, repository: EntityRepository[Achievement]):
        super().__init__(repository)

    @abstractmethod
    def get_details(self, id: int, lang_code: str) -> Optional[AchievementDetailsDTO]:
        pass


class AchievementService(IAchievementService):
    @inject
    def __init__(self, repository: EntityRepository[Achievement]):
        super().__init__(repository)

    def get_details(self, id: int, lang_code: LanguageCode):
        schema = AchievementDetailsSchema()
        achievements = self.get_all()

        for achievement in achievements:
            for description in achievement.descriptions:
                if description.language.code == lang_code.value:
                    achievement_dto = AchievementDetailsDTO(id=achievement.id, name=description.name,
                                                            scores=achievement.scores, text=description.text)
                    return schema.dump(achievement_dto)

        return None
