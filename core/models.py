from datetime import datetime

from sqlalchemy import Integer, Column, String, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from dal.context import Base


class UserAchievements(Base):
    __tablename__ = 'user_achievements'
    user_id = Column("user_id", Integer, ForeignKey("users.id"), primary_key=True)
    achievement_id = Column("achievement_id", Integer, ForeignKey("achievements.id"), primary_key=True)
    issued_at = Column("issued_at", DateTime, default=datetime.now, nullable=False)

    user = relationship('User', back_populates="user_achievements")
    achievement = relationship('Achievement', back_populates="user_achievements")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    language_id = Column(Integer, ForeignKey("languages.id"))

    user_achievements = relationship("UserAchievements", back_populates="user", cascade="all, delete-orphan")
    language = relationship("Language", back_populates='users')

    @property
    def achievements(self):
        # Находим все связи, в которых есть пользователь
        user_relations = [relation for relation in self.user_achievements if relation.user_id == self.id]
        # Получаем достижения из каждой связи
        achievements = [relation.achievement for relation in user_relations]

        return achievements


class Achievement(Base):
    __tablename__ = 'achievements'
    id = Column(Integer, primary_key=True)
    scores = Column(Integer, nullable=False)
    user_achievements = relationship("UserAchievements", back_populates="achievement", cascade="all, delete-orphan")
    descriptions = relationship("AchievementDescription", back_populates="achievement", cascade="all, delete-orphan")

    @property
    def users(self):
        # Находим все связи, в которых есть достижение
        achievement_relations = [relation for relation in self.user_achievements if relation.achievement_id == self.id]
        # Получаем пользователей из каждой связи
        users = [relation.user for relation in achievement_relations]

        return users


class Language(Base):
    __tablename__ = 'languages'
    id = Column(Integer, primary_key=True)
    code = Column(String(2), unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)

    achievements = relationship("AchievementDescription", back_populates="language")
    users = relationship("User", back_populates="language")


class AchievementDescription(Base):
    __tablename__ = 'achievements_descriptions'
    id = Column(Integer, primary_key=True)
    achievement_id = Column(Integer, ForeignKey("achievements.id"))
    language_id = Column(Integer, ForeignKey("languages.id"))
    name = Column(String, unique=True, nullable=False)
    text = Column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint('language_id', 'achievement_id', name='uq_achievement_language'),
    )

    language = relationship("Language", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="descriptions")
