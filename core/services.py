import abc
from typing import TypeVar, List

from dal.repositories import EntityRepository

T = TypeVar('T')


class Service(abc.ABC):
    _repository: EntityRepository[T]

    def __init__(self, repository: EntityRepository[T]):
        self._repository = repository

    def get(self, id: int) -> List[T]:
        return self._repository.get(id)
