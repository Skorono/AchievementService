import abc
from typing import List, Optional, Generic, TypeVar

from sqlalchemy.orm import Session

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

    def add_range(self, items: List[T]):
        self._session.add_all(items)
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

    def __del__(self):
        self._session.close()
