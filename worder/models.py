from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from sqlalchemy import Date, Integer

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    words = relationship("UserWord", back_populates="user")
    last_learn_date = Column(Date)  # Дата последнего изучения
    words_learned_today = Column(Integer, default=0)  # Сколько слов выучено сегодня


class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True)
    english = Column(String, nullable=False)
    russian = Column(String, nullable=False)


class UserWord(Base):
    __tablename__ = "user_words"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    word_id = Column(Integer, ForeignKey("words.id"))
    next_review = Column(DateTime, default=datetime.utcnow)
    interval = Column(Integer, default=1)  # В днях
    user = relationship("User", back_populates="words")
    word = relationship("Word")
