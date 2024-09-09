import abc
from typing import TypeVar, Generic, Optional, List, Callable

from injector import inject

from dal.repositories.repository import EntityRepository

T = TypeVar('T')


class Service(abc.ABC, Generic[T]):
    _repository: EntityRepository[T]

    @inject
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
