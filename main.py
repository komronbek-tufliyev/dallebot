from aiogram import types, executor, Bot, Dispatcher, exceptions
from aiogram.dispatcher import filters
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import re
from config import TG_API_TOKEN, API_KEY, ADMIN_IDS
from dalle_client import DallEClient

# keyboards to set up
from keyboards.language_settings import lang_settings
from keyboards.image_settings import size_menu_buttons, image_settings_menu
from keyboards.generated_image_buttons import main_image_buttons

# Main bot
from main_bot_obj import TgBot

# Bot database 
# from bot_db import session, User, Image, Sent_Message, create as create_table, delete as delete_table

logging.basicConfig(
    filename='my_bot.log', # Specifies the filename for the log file
    level=logging.INFO, # Specifies the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' # Specifies the format for the log messages
)

bot = Bot(token=TG_API_TOKEN)
dp = Dispatcher(bot=bot)

dalle_client = DallEClient(API_KEY=API_KEY)
Image_size = "1024x1024"
Number_of_images = 1

@dp.message_handler(commands=['start', 'help'])
async def start_help(message: types.Message):
    # engine() # creates database tables

    # user_id = message.from_user.id
    # full_name = message.from_user.full_name
    # username = message.from_user.username 
    # try:
        # user = User(full_name=full_name, username=username, tg_id=user_id)
        # create_table(user)
        # print("User saved successfully")
    # except Exception as e:
        # print("Error", e)
        # pass
        
    print(message.from_user.get_mention(name="Komronbek"))

    answer_message = "🖐Assalomu alaykum, \n🖼 men matnlar yordamida rasm generatsiya qila olaman. Sizga qanday yordam bera olaman! \n\n 🖐Hello, I can generate images from your text. How can I help you?"
    await message.answer(answer_message)


@dp.message_handler(commands=['settings'])
async def language_settings(message: types.Message):
    """
        This method replies to user with language settings inline buttons
    """
    lang_settings_buttons = lang_settings()
    answer = "Tilni tanlang ⬇️"
    # print("Lang settins", lang_settings_buttons)
    await message.reply(answer, reply_markup=lang_settings_buttons)


@dp.callback_query_handler(text_startswith="lang")
async def get_language_callback_query(callback_query: types.CallbackQuery):
    """
        This method gets language and sets up main bot (TgBot) language
    """
    callback_data = callback_query.data
    print("Callback data", callback_data)
    
    tg_bot = TgBot()

    # await callback_query.answer()
    lang = tg_bot.setup_lang(language=callback_data) # set up language 
    await callback_query.answer(f"Bot language changed to {lang}") 
    print("Lang", lang)
    await callback_query.message.delete() # delete last sent user message

    
@dp.message_handler(commands=['image_settings'])
async def image_settings(message: types.Message):
    keyboard = image_settings_menu()
    answer_text = "Tanlang\nSize - rasm o'lchami\nNumber of images - generatsiya qilinadigan rasmlar soni"
    await message.reply(answer_text, reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Size")
async def handle_sizes_list(message: types.Message):
    keyboard = size_menu_buttons()
    answer_text = "size choices"
    await message.reply(answer_text, reply_markup=keyboard)



@dp.message_handler(regexp=r"^(\d+x\d+)")
async def handle_size(message: types.Message):
    size = re.search(r"^(\d+x\d+)", message.text).group(1)
    print("size: ", size)
    Image_size = str(size)
    await message.reply(f"Image Size: {size}")
    

@dp.message_handler(filters.Text(equals="Back"))
async def back_image_settings(message: types.Message):
    keyboard = image_settings_menu()
    answer_text = "Tanlang\nSize - rasm o'lchami\nNumber of images - generatsiya qilinadigan rasmlar soni"
    await message.reply(answer_text, reply_markup=keyboard)


# A message handler to generate images.  
@dp.message_handler(filters.Text(startswith="/imagine"))
async def generate_image(message: types.Message):
    """
        Image generation handler. 
        This method gets these parameters: prompt(prompt), size(--size), number_of_image(--n).
        And calls generate_samples(prompt, number_of_image, size) function and 
        returns image to user with inline keyboard buttons(variations, download, edit)

    """
    message_answer = ""
    size = ""
    number_of_sample = 1
    Image_size = "1024x1024"
    try:
        match_size = re.search(r"--size (\d+x\d+)", message.text)
        if match_size:
            size = match_size.group(1)
            Image_size = str(size)
            print("size:", Image_size)
        else:
            print("No parameters found.")
        number_of_sample_match = re.search(r"--n (\d+)", message.text)
        if number_of_sample_match:
            number_of_sample = number_of_sample_match.group(1)
            Number_of_images = str(number_of_sample)
            print("number:", Number_of_images)
        else:
            print("No parameters found.")
        # number_of_sample = message.text.replace("--n",)
        prompt = re.sub(r"--size \d+x\d+|--n \d+", "", message.text)
        prompt = prompt.replace("/imagine ", "")
        print(prompt)

        message_answer = f"Generated image for: \n<b>{prompt}</b> 👇⬇️"
        print("prompt:", prompt)
        await message.reply(message_answer, parse_mode="HTML")
        

        if size:
            size = Image_size
        else: 
            size = "1024x1024"
        if not number_of_sample:
            number_of_sample = 1
        image_path = dalle_client.create_sample(prompt=prompt, size=Image_size, number=int(number_of_sample))
        print("Image path", image_path)
        with open(image_path, "rb") as image_file:
            image = types.InputFile(image_file)
            await message.reply_photo(photo=image, reply_markup=main_image_buttons())
        # dalle_client = DallEClient(API_KEY=API_KEY)
        # dalle_client.create_sample(prompt=prompt, number=number_of_sample)
    except exceptions.BadRequest as e:
        print("Error", e)
        message_answer = "Cannot generate image"
        await message.reply(message_answer, parse_mode="HTML")
        pass

@dp.callback_query_handler()
async def send_as_file(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == "send_as_file":
        await callback_query.answer("Telefonda yuklash tugmasi yo'qmikan 😲?!")
    elif data == "generate_other":
        await callback_query.answer("Gapni /imagine deb boshlash kerak")
    #    await callback_query.message.reply_document(document=)

@dp.message_handler(commands=['admin', 'superadmin'])
async def admin_page(message: types.Message):
    user_id = message.from_user.id
    answer_text = ""
    if str(user_id) in ADMIN_IDS:
        members = await bot.get_chat_members_count(chat_id=message.chat.id)
        answer_text = f"🧑‍💻Here admin page url: Admin_page_url. Your bot have {members} members"
    else:
        answer_text = "🚫Only admins have access!"
    await message.reply(answer_text)


@dp.message_handler()
async def echo(message: types.Message):
    await message.reply(message.text)



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)