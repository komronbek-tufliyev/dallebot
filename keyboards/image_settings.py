from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

def image_settings_menu():
    
    menu_buttons = [
        [KeyboardButton("Size"), KeyboardButton("Number of images")]
    ]
    menu = ReplyKeyboardMarkup(keyboard=menu_buttons, resize_keyboard=True, one_time_keyboard=True)
    return menu

def size_menu_buttons():
    buttons = [ 
        [KeyboardButton("256x256"), KeyboardButton("512x512"), KeyboardButton("1024x1024")],
        [KeyboardButton("Back"), KeyboardButton("Main menu")]
    ]
    menu = ReplyKeyboardMarkup(keyboard=buttons, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Enter", selective=True)
    return menu

def number_menu_buttons():
    buttons = [
        [KeyboardButton("1"), KeyboardButton("2"), KeyboardButton("3"), KeyboardButton("4")],
    ]