from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    words = relationship("UserWord", back_populates="user")
    last_learn_date = Column(Date)  # Дата последнего изучения
    words_learned_today = Column(Integer, default=0)  # Сколько слов выучено сегодня
    words_per_day = Column(Integer, default=10)  # Новых слов в день
    repeat_multiplier = Column(Integer, default=2)  # Множитель интервала


class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)  # Английское слово
    translation = Column(String, nullable=False)  # Перевод
    level = Column(String, nullable=False)


class UserWord(Base):
    __tablename__ = 'user_words'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    word_id = Column(Integer, ForeignKey('words.id'))
    next_review = Column(DateTime, default=datetime.utcnow)
    interval = Column(Integer, default=1)
    correct_count = Column(Integer, default=0)    # число успешных повторений
    error_count = Column(Integer, default=0)      # число ошибок
    first_learned = Column(DateTime, default=datetime.utcnow)  # когда впервые выдано
    last_reviewed = Column(DateTime, default=None)             # когда в последний раз повторялось
    user = relationship('User', back_populates='words')
    word = relationship('Word')
