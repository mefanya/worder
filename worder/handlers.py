from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Update,
)
from telegram.ext import ContextTypes
from datetime import datetime, timedelta, date
from .db import Session
from .models import User, Word, UserWord
from .menu import get_main_menu
from .words_loader import load_words

WORDS = load_words()


async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Учить слово":
        await learn(update, context)
    elif text == "Повторить слова":
        await review(update, context)
    elif text == "Тест":
        await update.message.reply_text("Тесты скоро появятся!")
    elif text == "Мой прогресс":
        await update.message.reply_text("Статистика в разработке.")
    else:
        await update.message.reply_text(
            "Пожалуйста, выбери действие с помощью кнопок.",
            reply_markup=get_main_menu(),
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    session = Session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id)
        session.add(user)
        session.commit()
    await update.message.reply_text(
        "Привет! Я помогу тебе учить английские слова.", reply_markup=get_main_menu()
    )
    session.close()


async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message or update.effective_message
    telegram_id = update.effective_user.id
    session = Session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    today = date.today()

    if user.last_learn_date != today:
        user.last_learn_date = today
        user.words_learned_today = 0
        session.commit()

    if user.words_learned_today >= 10:
        await message.reply_text(
            "Сегодня ты уже выучил 10 новых слов! Приходи завтра за следующей порцией."
        )
        session.close()
        return

    for idx, w in enumerate(WORDS):
        word = session.query(Word).filter_by(english=w["english"]).first()
        if not word:
            word = Word(english=w["english"], russian=w["russian"])
            session.add(word)
            session.commit()
        if (
            not session.query(UserWord)
            .filter_by(user_id=user.id, word_id=word.id)
            .first()
        ):
            user_word = UserWord(
                user_id=user.id,
                word_id=word.id,
                next_review=datetime.utcnow() + timedelta(days=1),
            )
            session.add(user_word)
            user.words_learned_today += 1
            session.commit()
            ordinal = f"{user.words_learned_today}-е слово"
            text = (
                f"{ordinal}:\n\n"
                f"{w['english']} - {w['russian']}\n\n"
                f"> {w['example']}\n"
                f"> {w['example_russian']}"
            )
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("Дальше", callback_data="next_word")]]
            )
            await message.reply_text(text, reply_markup=keyboard)
            break
    else:
        await message.reply_text("Ты выучил все слова!")
    session.close()


async def review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    session = Session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    now = datetime.utcnow()
    words_for_review = (
        session.query(UserWord)
        .filter_by(user_id=user.id)
        .filter(UserWord.next_review <= now)
        .all()
    )
    if not words_for_review:
        await update.message.reply_text("Сегодня нет слов для повторения!")
    for uw in words_for_review:
        await update.message.reply_text(f"Вспомни перевод: {uw.word.english}")
        uw.interval *= 2
        uw.next_review = now + timedelta(days=uw.interval)
        session.commit()
    session.close()


async def next_word_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await learn(update, context)
