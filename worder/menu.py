from telegram import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu():
    keyboard = [
        [KeyboardButton("Учить слово"), KeyboardButton("Повторить слова")],
        [KeyboardButton("Тест"), KeyboardButton("Мой прогресс")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
