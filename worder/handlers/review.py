from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
from ..db import Session
from ..models import User, UserWord

async def review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = Session()
    user = session.query(User).filter_by(telegram_id=update.effective_user.id).first()
    if not user:
        await update.message.reply_text("Сначала изучите слова.")
        session.close(); return

    now = datetime.utcnow()
    dues = session.query(UserWord).filter(
        UserWord.user_id==user.id,
        UserWord.next_review<=now
    ).all()
    if not dues:
        await update.message.reply_text("Нет слов для повторения!")
    else:
        for uw in dues:
            await update.message.reply_text(f"Вспомните: {uw.word.word}")
            uw.interval *= user.repeat_multiplier
            uw.next_review = now + timedelta(days=uw.interval)
            session.commit()
    session.close()
