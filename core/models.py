from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class UserAchievements(Base):
    __tablename__ = 'user_achievements'
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), primary_key=True)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    language_id = Column(Integer, ForeignKey("languages.id"))
    achievements = relationship("Achievements", secondary=UserAchievements, back_populates="users")


class Achievement(Base):
    _tablename__ = 'achievements'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    users = relationship("User", secondary=UserAchievements, back_populates="achievements")
    descriptions = relationship("AchievementDescription", back_populates="description")


class Language(Base):
    __tablename__ = 'languages'
    id = Column(Integer, primary_key=True)
    code = Column(String(2), unique=True)
    name = Column(String, unique=True)


class AchievementDescription(Base):
    __tablename__ = 'achievements_descriptions'
    id = Column(Integer, primary_key=True)
    achievement_id = Column(Integer, ForeignKey("achievements.id"))
    language_id = Column(Integer, ForeignKey("languages.id"))
    description = Column(String(1024))
    achievement = relationship("Achievement", back_populates="descriptions")
