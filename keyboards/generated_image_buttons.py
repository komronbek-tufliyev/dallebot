from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_image_buttons():
    menu = InlineKeyboardMarkup(row_width=2)
    text_and_data = (
        ("Send as file ⬇️", "send_as_file"),
        ("Generate one 🔄", "generate_other")
    )
    buttons = (InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    menu.row(*buttons)
    return menu
