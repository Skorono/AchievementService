import injector
from sqlalchemy.orm import Session

from core.models import Achievement
from dal.repositories.repository import EntityRepository


class AchievementRepository(EntityRepository[Achievement]):

    @injector.inject
    def __init__(self, session: Session, model=Achievement):
        super().__init__(session, model)
