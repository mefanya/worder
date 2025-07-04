from telegram import Update
from telegram.ext import ContextTypes
from ..db import Session
from ..models import User
from ..menu import get_main_menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = Session()
    telegram_id = update.effective_user.id
    if not session.query(User).filter_by(telegram_id=telegram_id).first():
        session.add(User(telegram_id=telegram_id))
        session.commit()
    await update.message.reply_text(
        "Привет! Я помогу тебе учить английские слова.",
        reply_markup=get_main_menu()
    )
    session.close()
