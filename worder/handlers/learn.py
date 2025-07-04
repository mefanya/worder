from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes
from datetime import datetime, timedelta, date
from ..db import Session
from ..models import User, Word, UserWord
from ..words_loader import load_words

WORDS = load_words()

async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Поддержка как обычных сообщений, так и callback_query
    if update.message:
        message = update.message
    else:
        message = update.callback_query.message
    session = Session()
    telegram_id = update.effective_user.id
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id)
        session.add(user); session.commit()

    today = date.today()
    if user.last_learn_date != today:
        user.last_learn_date = today
        user.words_learned_today = 0
        session.commit()

    if user.words_learned_today >= user.words_per_day:
        await message.reply_text(f"Лимит {user.words_per_day} исчерпан.")
        session.close()
        return

    for w in WORDS:
        word_obj = session.query(Word).filter_by(word=w["Word"]).first()
        if not word_obj:
            word_obj = Word(
                word=w["Word"],
                translation=w["Translation"],
                level=w["Level"]
            )
            session.add(word_obj); session.commit()
        if not session.query(UserWord).filter_by(user_id=user.id, word_id=word_obj.id).first():
            uw = UserWord(
                user_id=user.id,
                word_id=word_obj.id,
                next_review=datetime.utcnow() + timedelta(days=1)
            )
            session.add(uw)
            user.words_learned_today += 1
            session.commit()
            text = (
                f"{user.words_learned_today}-е слово:\n\n"
                f"{w['Word']} [{w.get('Pronunciation (RU)','')}] - {w['Translation']}\n\n"
                f"> {w['Example EN']}\n> {w['Example RU']}\n\n"
                f"Уровень: {w['Level']}"
            )
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("Дальше", callback_data="next_word")]])
            await message.reply_text(text, reply_markup=kb)
            break
    else:
        await message.reply_text("Все слова изучены!")
    session.close()
