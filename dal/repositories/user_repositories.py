import injector
from sqlalchemy.orm import Session

from core.models import User
from dal.repositories.repository import EntityRepository


class UserRepository(EntityRepository[User]):
    @injector.inject
    def __init__(self, session: Session, model=User):
        super().__init__(session, model)
