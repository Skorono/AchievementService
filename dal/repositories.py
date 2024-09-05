import abc
from typing import TypeVar, Optional, Generic, List

from sqlalchemy.orm import Session

T = TypeVar('T')


class EntityRepository(abc.ABC, Generic[T]):

    def __init__(self, session: Session):
        self.session = session

    def get(self, id: int) -> Optional[T]:
        pass

    def get_all(self) -> List[T]:
        pass

    def add(self, item: T) -> None:
        pass

    def delete(self, id: int) -> None:
        pass

    def update(self, item: T) -> None:
        pass
