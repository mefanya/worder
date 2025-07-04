from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from worder.db import TOKEN
from worder.handlers.start import start
from worder.handlers.learn import learn
from worder.handlers.review import review
from worder.handlers.menu import handle_menu
from worder.handlers.progress import (
    show_progress,
    show_overall_stats,
    show_achievements,
)
from worder.handlers.callbacks import next_word_callback

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # /start
    app.add_handler(CommandHandler("start", start))

    # Учить и повторить
    app.add_handler(MessageHandler(filters.Regex(r"^Учить слово$"), learn))
    app.add_handler(MessageHandler(filters.Regex(r"^Повторить слова$"), review))

    # Прогресс
    app.add_handler(MessageHandler(filters.Regex(r"^Мой прогресс$"), show_progress))
    app.add_handler(MessageHandler(filters.Regex(r"^Общая статистика$"), show_overall_stats))
    app.add_handler(MessageHandler(filters.Regex(r"^Достижения$"), show_achievements))

    # Настройки и навигация
    app.add_handler(MessageHandler(filters.Regex(
        r"^(Настройки|Сложность|Интервал повторения|Выйти в меню|Назад к настройкам)$"
    ), handle_menu))
    app.add_handler(MessageHandler(filters.Regex(r"^(10|20|30|40|50|2|3)$"), handle_menu))

    # Главное меню (fallback)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    # Inline «Дальше»
    app.add_handler(CallbackQueryHandler(next_word_callback, pattern=r"^next_word$"))

    app.run_polling()

if __name__ == "__main__":
    main()
