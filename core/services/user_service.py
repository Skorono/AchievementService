import abc
from typing import Optional, List

from flasgger import Schema
from injector import inject

from core.dtos.achievement_dto import AchievementDetailsSchema, AchievementDetailsDTO
from core.dtos.user_dto import UserSummarySchema
from core.enums.language_code import LanguageCode
from core.helpers.dto_transformer import DtoTransformer
from core.models import User, UserAchievements
from core.services.service import Service
from dal.repositories.repository import EntityRepository


class IUserService(Service[User]):
    @inject
    def __init__(self, repository: EntityRepository[User]):
        super().__init__(repository)

    @abc.abstractmethod
    def get_summary(self, id: int) -> Schema:
        pass

    @abc.abstractmethod
    def get_all_summary(self) -> Schema:
        pass

    @abc.abstractmethod
    def get_by_name(self, username: str) -> Optional[Schema]:
        """Возвращает dto пользователя по нику"""
        pass


class IUserStatisticService(Service[User]):
    @inject
    def __init__(self, repository: EntityRepository[User]):
        super().__init__(repository)

    @abc.abstractmethod
    def get_score_leader(self) -> Optional[Schema]:
        """Возвращает dto пользователя у которого больше всего очков"""
        pass

    @abc.abstractmethod
    def get_achievements_leader(self) -> Optional[Schema]:
        """Возвращает dto пользователя имеющего самое большое количество достижений"""
        pass

    @abc.abstractmethod
    def get_min_diff_users(self) -> List[Schema]:
        pass

    @abc.abstractmethod
    def get_weekly_streak_users(self):
        """Возвращает dto пользователей получавших достижения в течении недели"""
        pass


class IUserAchievementsService(Service[User]):
    @inject
    def __init__(self, repository: EntityRepository[User]):
        super().__init__(repository)
    @abc.abstractmethod
    def add_achievement(self, user_id: int, achievement_id: int):
        """Добавляет пользователю достижение"""
        pass

    @abc.abstractmethod
    def delete_achievement(self, user_id: int, achievement_id: int):
        """Удаляет достижение из списка достижений пользователя"""
        pass

    @abc.abstractmethod
    def get_achievements(self, user_id) -> Optional[List[Schema]]:
        """Возвращает dto достижений пользователя по id"""
        pass


class UserStatisticService(IUserStatisticService):

    @inject
    def __init__(self, repository: EntityRepository[User]):
        super().__init__(repository)

    def get_score_leader(self) -> UserSummarySchema:
        schema = UserSummarySchema()
        users = self._get_all()
        leader = max(users, key=lambda u: sum(a.scores for a in u.achievements))

        leader_dto = DtoTransformer.user_to_dto(leader)

        return schema.dump(leader_dto)

    def get_achievements_leader(self) -> UserSummarySchema:
        schema = UserSummarySchema()
        users = self._get_all()
        leader = max(users, key=lambda u: len(u.achievements))

        leader_dto = DtoTransformer.user_to_dto(leader)

        return schema.dump(leader_dto)

    def get_min_diff_users(self) -> UserSummarySchema:
        users = self._get_all()
        user_scores = [sum(achievement.scores for achievement in u.achievements) if len(u.achievements) != 0 else 0 for
                       u in users]

        min_diff = float('inf')
        min_diff_users = None

        for i in range(len(user_scores) - 1):
            diff = abs(user_scores[i] - user_scores[i + 1])
            if diff < min_diff:
                min_diff = diff
                min_diff_users = [users[i], users[i + 1]]

        users_dto = list(map(lambda u: DtoTransformer.user_to_dto(u), min_diff_users))
        return UserSummarySchema().dump(users_dto, many=True)

    def get_weekly_streak_users(self) -> UserSummarySchema:
        schema = UserSummarySchema()
        users = self._get_all()

        weakly_streak_users = list(filter(lambda u: print(), users))

        return schema.dump(weakly_streak_users, many=True)


class UserService(IUserService):
    def get_summary(self, id: int) -> UserSummarySchema:
        user_dto = DtoTransformer.user_to_dto(self._get(id))
        return UserSummarySchema().dump(user_dto)

    def get_all_summary(self) -> UserSummarySchema:
        users = DtoTransformer.users_to_dto(self._get_all())
        return UserSummarySchema().dump(users, many=True)

    def get_by_name(self, username: str) -> Optional[UserSummarySchema]:
        user = self._get_filtered(lambda u: u.username == username)[0]
        user_dto = UserSummarySchema().dump(user)

        return user_dto

    @inject
    def __init__(self, repository: EntityRepository[User]):
        super().__init__(repository)


class UserAchievementsService(IUserAchievementsService):
    @inject
    def __init__(self, repository: EntityRepository[User]):
        super().__init__(repository)

    def add_achievement(self, user_id, achievement_id):
        user = self._get(user_id)
        user.user_achievements.append(UserAchievements(user_id=user.id, achievement_id=achievement_id))

        self._repository.save()

    def get_achievements(self, user_id) -> AchievementDetailsSchema:
        schema = AchievementDetailsSchema()
        user: User = self._get(user_id)

        if user is None:
            return

        user_achievements_dto: List[AchievementDetailsDTO] = \
            DtoTransformer.achievements_to_dto(user.achievements, language=LanguageCode[user.language.code])

        for achievement_relation in user.user_achievements:
            # Находим первый элемент коллекции с подходящим id и добавляем ему дату выдачи
            # Предполагается, что такой элемент точно должен существовать, так что next не обрабатывается
            achievement_dto = next((a for a in user_achievements_dto if a.id == achievement_relation.achievement.id))
            achievement_dto.issued_at = achievement_relation.issued_at

        return schema.dump(user_achievements_dto, many=True)

    def delete_achievement(self, user_id: int, achievement_id: int) -> None:
        user = self._get(user_id)
        user_achievement_relation = (
            next((relation for relation in user.user_achievements if relation.achievement_id == achievement_id), None))

        user.user_achievements.remove(user_achievement_relation)
        self._repository.save()