from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    return ReplyKeyboardMarkup([
        [KeyboardButton("Учить слово"), KeyboardButton("Повторить слова")],
        [KeyboardButton("Мой прогресс"), KeyboardButton("Настройки")]
    ], resize_keyboard=True)

def get_settings_menu():
    return ReplyKeyboardMarkup([
        [KeyboardButton("Сложность")],
        [KeyboardButton("Интервал повторения")],
        [KeyboardButton("Выйти в меню")]
    ], resize_keyboard=True)

def get_difficulty_menu():
    return ReplyKeyboardMarkup([
        [KeyboardButton("10"), KeyboardButton("20"), KeyboardButton("30")],
        [KeyboardButton("40"), KeyboardButton("50")],
        [KeyboardButton("Назад к настройкам")]
    ], resize_keyboard=True)

def get_repeat_menu():
    return ReplyKeyboardMarkup([
        [KeyboardButton("2"), KeyboardButton("3")],
        [KeyboardButton("Назад к настройкам")]
    ], resize_keyboard=True)

def get_progress_menu():
    return ReplyKeyboardMarkup([
        [KeyboardButton("Общая статистика"),KeyboardButton("Достижения")],
         [KeyboardButton("Назад в меню")]
    ], resize_keyboard=True)
