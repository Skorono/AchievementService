import abc
from typing import TypeVar, List, Optional, Generic, Callable

import injector

from core.models import User, Achievement
from dal.repositories import EntityRepository

T = TypeVar('T')


class Service(abc.ABC, Generic[T]):
    _repository: EntityRepository[T]

    @injector.inject
    def __init__(self, repository: EntityRepository[T]):
        self._repository = repository

    def get(self, id: int) -> Optional[T]:
        return self._repository.get(id)

    def get_all(self) -> List[T]:
        return self._repository.get_all()

    def get_filtered(self, predicate: Callable[[T], bool]) -> List[T]:
        entities = self._repository.get_all()
        return list(filter(predicate, entities))

    def add(self, entity: T) -> None:
        self._repository.add(entity)

    def update(self, entity: T) -> None:
        self._repository.update(entity)

    def delete(self, id: int) -> None:
        self._repository.delete(id)


class UserServiceBase(Service[User]):
    @injector.inject
    def __init__(self, repository: EntityRepository[User]):
        super().__init__(repository)

    @abc.abstractmethod
    def get_achievements(self, user_id) -> Optional[List[Achievement]]:
        pass

    @abc.abstractmethod
    def get_score_leader(self, user_id: int) -> Optional[User]:
        pass

    @abc.abstractmethod
    def get_achievements_leader(self, user_id: int) -> Optional[User]:
        pass

    @abc.abstractmethod
    def get_min_diff_users(self):
        pass

    @abc.abstractmethod
    def get_weekly_streak_users(self):
        pass


class UserService(UserServiceBase):
    def get_achievements(self, user_id) -> Optional[List[Achievement]]:
        pass

    def get_score_leader(self, user_id: int) -> Optional[User]:
        pass

    def get_achievements_leader(self, user_id: int) -> Optional[User]:
        pass

    def get_min_diff_users(self):
        pass

    def get_weekly_streak_users(self):
        pass

    @injector.inject
    def __init__(self, repository: EntityRepository[User]):
        super().__init__(repository)


class AchievementServiceBase(abc.ABC, Service[Achievement]):
    @injector.inject
    def __init__(self, repository: EntityRepository[Achievement]):
        super().__init__(repository)


class AchievementService(Service[Achievement]):
    @injector.inject
    def __init__(self, repository: EntityRepository[Achievement]):
        super().__init__(repository)
