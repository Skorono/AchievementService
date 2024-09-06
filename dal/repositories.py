import abc
from typing import TypeVar, Optional, Generic, List

import injector
from sqlalchemy.orm import Session

from core.models import User, Achievement

T = TypeVar('T')


class EntityRepository(abc.ABC, Generic[T]):
    def __init__(self, session: Session, model: T):
        self._session = session
        self._model = model

    def get(self, id: int) -> Optional[T]:
        return self._session.query(self._model).get(id)

    def get_all(self) -> List[T]:
        return self._session.query(self._model).all()

    def add(self, item: T) -> None:
        self._session.add(item)
        self.save()

    def delete(self, id: int) -> None:
        entity = self.get(id)
        if entity:
            self._session.delete(entity)
            self.save()

    def update(self, item: T) -> None:
        self._session.merge(item)
        self.save()

    def save(self) -> None:
        self._session.commit()


class UserRepository(EntityRepository[User]):
    @injector.inject
    def __init__(self, session: Session, model=User):
        super().__init__(session, model)


class AchievementRepository(EntityRepository[Achievement]):

    @injector.inject
    def __init__(self, session: Session, model=Achievement):
        super().__init__(session, model)
