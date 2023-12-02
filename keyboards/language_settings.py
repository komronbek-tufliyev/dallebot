from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def lang_settings():
    start_keyboard_markup = InlineKeyboardMarkup(row_width=2)
    text_and_data = (
        ("O'zbek 🇺🇿", "lang_uzb"),
        ("English 🇬🇧", "lang_en"),
        # ("Russian 🇷🇺", "lang_ru")
    )

    row_btns = (InlineKeyboardButton(text=text, callback_data=data) for text, data in text_and_data)
    start_keyboard_markup.row(*row_btns)

    return start_keyboard_markup
