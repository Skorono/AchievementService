import abc
from typing import Optional, List

from injector import inject

from core.dtos.achievement_dto import AchievementDetailsSchema, AchievementDetailsDTO
from core.dtos.user_dto import UserSummarySchema
from core.enums.language_code import LanguageCode
from core.helpers.dto_transformer import DtoTransformer
from core.models import User
from core.services.service import Service
from dal.repositories.repository import EntityRepository


class IUserService(Service[User]):
    @inject
    def __init__(self, repository: EntityRepository[User]):
        super().__init__(repository)

    @abc.abstractmethod
    def get_achievements(self, user_id) -> Optional[List[AchievementDetailsSchema]]:
        pass

    @abc.abstractmethod
    def get_score_leader(self) -> Optional[UserSummarySchema]:
        pass

    @abc.abstractmethod
    def get_achievements_leader(self, user_id: int) -> Optional[UserSummarySchema]:
        pass

    @abc.abstractmethod
    def get_min_diff_users(self):
        pass

    @abc.abstractmethod
    def get_weekly_streak_users(self):
        pass


class UserService(IUserService):
    def get_achievements(self, user_id):
        schema = AchievementDetailsSchema()
        user: User = self.get(user_id)
        user_achievements_dto: List[AchievementDetailsDTO] = \
            DtoTransformer.achievements_to_dto(user.achievements, language=LanguageCode[user.language.name])

        return schema.dump(user_achievements_dto, many=True)

    def get_score_leader(self):
        schema = UserSummarySchema()
        users = self.get_all()
        leader = users[0]
        (lambda u: map(lambda a: print(a.scores), u.achievements))(users[0])

        leader_dto = DtoTransformer.user_to_dto(leader)

        return schema.dump(leader_dto)

    def get_achievements_leader(self, user_id: int) -> Optional[User]:
        pass

    def get_min_diff_users(self):
        pass

    def get_weekly_streak_users(self):
        pass

    @inject
    def __init__(self, repository: EntityRepository[User]):
        super().__init__(repository)
