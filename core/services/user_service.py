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
    def get_achievements_leader(self) -> Optional[UserSummarySchema]:
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
            DtoTransformer.achievements_to_dto(user.achievements, language=LanguageCode[user.language.code])

        for achievement_relation in user.user_achievements:
            # Находим первый элемент коллекции с подходящим id и добавляем ему дату выдачи
            # Предполагается, что такой элемент точно должен существовать, так что next не обрабатывается
            achievement_dto = next((a for a in user_achievements_dto if a.id == achievement_relation.achievement.id))
            achievement_dto.issued_at = achievement_relation.issued_at

        return schema.dump(user_achievements_dto, many=True)

    def get_score_leader(self):
        schema = UserSummarySchema()
        users = self.get_all()
        leader = max(users, key=lambda u: sum(a.scores for a in u.achievements))

        leader_dto = DtoTransformer.user_to_dto(leader)

        return schema.dump(leader_dto)

    def get_achievements_leader(self):
        schema = UserSummarySchema()
        users = self.get_all()
        leader = max(users, key=lambda u: len(u.achievements))

        leader_dto = DtoTransformer.user_to_dto(leader)

        return schema.dump(leader_dto)

    def get_min_diff_users(self):
        pass

    def get_weekly_streak_users(self):
        schema = UserSummarySchema()
        users = self.get_all()

        weakly_streak_users = list(filter(lambda u: print(), users))

        return schema.dump(weakly_streak_users, many=True)

    @inject
    def __init__(self, repository: EntityRepository[User]):
        super().__init__(repository)
