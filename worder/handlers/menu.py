from telegram import Update
from telegram.ext import ContextTypes
from ..db import Session
from ..models import User
from ..menu import (
    get_main_menu,
    get_settings_menu,
    get_difficulty_menu,
    get_repeat_menu
)

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    session = Session()
    telegram_id = update.effective_user.id
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        session.add(User(telegram_id=telegram_id))
        session.commit()

    if text == "Настройки":
        await update.message.reply_text("Настройки:", reply_markup=get_settings_menu())
    elif text == "Сложность":
        await update.message.reply_text("Сколько слов в день?", reply_markup=get_difficulty_menu())
    elif text in ["10", "20", "30", "40", "50"]:
        user.words_per_day = int(text); session.commit()
        await update.message.reply_text(f"{text} слов в день.", reply_markup=get_settings_menu())
    elif text == "Интервал повторения":
        await update.message.reply_text("Множитель:", reply_markup=get_repeat_menu())
    elif text in ["2", "3"]:
        user.repeat_multiplier = int(text); session.commit()
        await update.message.reply_text(f"×{text}", reply_markup=get_settings_menu())
    elif text == "Выйти в меню":
        await update.message.reply_text("Главное меню:", reply_markup=get_main_menu())
    elif text == "Назад к настройкам":
        await update.message.reply_text("Настройки:", reply_markup=get_settings_menu())
    else:
        # обрабатываем другие кнопки через главный меню-хендлер
        await update.message.reply_text("Выберите действие:", reply_markup=get_main_menu())

    session.close()
