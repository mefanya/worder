from telegram import Update
from telegram.ext import ContextTypes
from datetime import date, datetime, timedelta
from ..db import Session
from ..models import UserWord, User
from ..menu import get_progress_menu
from ..words_loader import load_words

ALL_WORDS = []

def _load_all():
    global ALL_WORDS
    if not ALL_WORDS:
        ALL_WORDS = load_words()
    return ALL_WORDS

async def show_progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    session = Session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()

    # Общая статистика
    total_learned = session.query(UserWord).filter_by(user_id=user.id).count()
    # Сегодня/неделя/месяц
    today = date.today()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    learned_today = session.query(UserWord).filter(
        UserWord.user_id==user.id,
        UserWord.first_learned>=datetime(today.year,today.month,today.day)
    ).count()
    learned_week = session.query(UserWord).filter(
        UserWord.user_id==user.id,
        UserWord.first_learned>=datetime(week_ago.year,week_ago.month,week_ago.day)
    ).count()
    learned_month = session.query(UserWord).filter(
        UserWord.user_id==user.id,
        UserWord.first_learned>=datetime(month_ago.year,month_ago.month,month_ago.day)
    ).count()

    # График ASCII роста (последние 7 дней)
    counts = []
    labels = []
    for i in range(7):
        d = today - timedelta(days=6-i)
        cnt = session.query(UserWord).filter(
            UserWord.user_id==user.id,
            UserWord.first_learned>=datetime(d.year,d.month,d.day),
            UserWord.first_learned< datetime(d.year,d.month,d.day)+timedelta(days=1)
        ).count()
        counts.append(cnt)
        labels.append(d.strftime('%d.%m'))
    max_cnt = max(counts) or 1
    chart = "\n".join(f"{labels[i]}: " + "█" * (counts[i]*10//max_cnt) + f" {counts[i]}" for i in range(7))

    # Устойчивые слова (highest interval)
    stable = session.query(UserWord).filter_by(user_id=user.id).order_by(UserWord.interval.desc()).limit(5).all()
    stable_list = "\n".join(f"{uw.word.word} (интервал {uw.interval} дн.)" for uw in stable)

    # Достижения
    # 7 дней подряд?
    streak = 0
    for i in range(7):
        d = today - timedelta(days=i)
        cnt = session.query(UserWord).filter(
            UserWord.user_id==user.id,
            UserWord.first_learned>=datetime(d.year,d.month,d.day),
            UserWord.first_learned< datetime(d.year,d.month,d.day)+timedelta(days=1)
        ).count()
        if cnt>0: streak+=1
        else: break
    achievements = f"Текущая серия дней: {streak}\nВсего слов: {total_learned}"
    if total_learned>=100:
        achievements += "\n🏅 Достижение: 100 слов выучено!"

    # CEFR прогресс
    levels = {}
    for uw in session.query(UserWord).filter_by(user_id=user.id).all():
        lvl = uw.word.level  # предполагаем, что у Word есть поле level
        levels[lvl] = levels.get(lvl,0)+1
    cefr_list = "\n".join(f"{lvl}: {cnt}" for lvl,cnt in levels.items())

    # Прогресс-бар
    all_words = _load_all()
    total_dict = len(all_words)
    percent = (total_learned / total_dict * 100) if total_dict else 0.0
    percent_str = f"{percent:.2f}"
    filled_blocks = int(percent // 10)
    progress_bar = "█" * filled_blocks + "-" * (10 - filled_blocks) + f" {percent_str}%"

    msg = (
        f"📊 Общая статистика:\n"
        f"Всего выучено: {total_learned}\n"
        f"Сегодня: {learned_today}, Неделя: {learned_week}, Месяц: {learned_month}\n\n"
        f"📈 Рост за 7 дней:\n{chart}\n\n"
        f"💪 Устойчивые слова:\n{stable_list or '—'}\n\n"
        f"🏆 Достижения:\n{achievements}\n\n"
        f"📚 CEFR прогресс:\n{cefr_list or '—'}\n\n"
        f"🔖 Прогресс словаря:\n{progress_bar}"
    )
    await update.message.reply_text(msg, reply_markup=get_progress_menu())
    session.close()

async def show_overall_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = Session()
    user = session.query(User).filter_by(telegram_id=update.effective_user.id).first()
    total = session.query(UserWord).filter_by(user_id=user.id).count()
    await update.message.reply_text(
        f"Всего выучено слов: {total}",
        reply_markup=get_progress_menu()
    )
    session.close()
    


async def show_achievements(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает достижения пользователя: серия дней и 100+ выученных слов."""
    session = Session()
    user = session.query(User).filter_by(telegram_id=update.effective_user.id).first()

    # Общее число выученных слов
    total = session.query(UserWord).filter_by(user_id=user.id).count()

    # Расчёт серии подряд идущих дней
    streak = 0
    today = date.today()
    for i in range(7):
        d = today - timedelta(days=i)
        count = session.query(UserWord).filter(
            UserWord.user_id==user.id,
            UserWord.first_learned>=datetime(d.year, d.month, d.day),
            UserWord.first_learned< datetime(d.year, d.month, d.day) + timedelta(days=1)
        ).count()
        if count > 0:
            streak += 1
        else:
            break

    msg = f"🏆 Текущая серия дней: {streak}\n📚 Всего выучено слов: {total}"
    if total >= 100:
        msg += "\n🎉 Достижение: выучено 100 слов!"

    await update.message.reply_text(msg, reply_markup=get_progress_menu())
    session.close()
    
    