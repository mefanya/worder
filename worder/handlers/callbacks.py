from telegram import Update
from telegram.ext import ContextTypes
from .learn import learn

async def next_word_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await learn(update, context)
