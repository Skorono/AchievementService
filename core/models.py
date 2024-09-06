from sqlalchemy import Integer, Column, String, DateTime, ForeignKey, Table, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

user_achievements = Table(
    "user_achievements",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("achievement_id", Integer, ForeignKey("achievements.id"), primary_key=True),
    Column("created_at", DateTime)
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    language_id = Column(Integer, ForeignKey("languages.id"))
    achievements = relationship("Achievement", secondary=user_achievements, back_populates="users")


class Achievement(Base):
    __tablename__ = 'achievements'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    scores = Column(Integer)
    users = relationship("User", secondary=user_achievements, back_populates="achievements")
    descriptions = relationship("AchievementDescription", back_populates="achievement")


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
    description = Column(Text(1024))
    achievement = relationship("Achievement", back_populates="descriptions")
