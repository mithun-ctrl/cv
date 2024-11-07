from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config import BOT_OWNER
from plugins.pin import pin_button_callback

# Callback handlers for the buttons
@Client.on_callback_query(filters.regex("^(about|home|help|support|back)$"))
async def button_callback(client, callback_query):
    data = callback_query.data
    chat_id = callback_query.message.chat.id

    if data == "about":
        about_text = "This bot is built using the Pyrogram library. It was created by your_name."
        await callback_query.message.edit_text(about_text)
    elif data == "home":
        start_text = "Welcome to the admin bot! Use the buttons below to navigate."
        await callback_query.message.edit_text(start_text, reply_markup=callback_query.message.reply_markup)
    elif data == "help":
        pin_button = InlineKeyboardButton("Pin", callback_data="pin")
        help_keyboard = InlineKeyboardMarkup([[pin_button]])
        help_text = "Here are the available commands:\n\n/pin - Pins the message\n/unpin - Unpins the message\n/pinned - Gets the currently pinned message"
        await callback_query.message.edit_text(help_text, reply_markup=help_keyboard)
    elif data == "support":
        chat1_link = "https://t.me/your_chat1"
        chat2_link = "https://t.me/your_chat2"
        support_text = "If you need any help, you can reach out to us at the following channels:"
        support_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Chat 1", url=chat1_link)],
            [InlineKeyboardButton("Chat 2", url=chat2_link)]
        ])
        await callback_query.message.edit_text(support_text, reply_markup=support_keyboard)
    elif data == "back":
        start_text = "Welcome to the admin bot! Use the buttons below to navigate."
        await callback_query.message.edit_text(start_text, reply_markup=callback_query.message.reply_markup)

# /start command
@Client.on_message(filters.command("start"))
async def start_command(client, message: Message):
    about_button = InlineKeyboardButton("About", callback_data="about")
    home_button = InlineKeyboardButton("Home", callback_data="home")
    help_button = InlineKeyboardButton("Help", callback_data="help")
    support_button = InlineKeyboardButton("Support", callback_data="support")
    back_button = InlineKeyboardButton("Back", callback_data="back")

    keyboard = InlineKeyboardMarkup([
        [about_button, home_button],
        [help_button, support_button],
        [back_button]
    ])

    start_text = "Welcome to the admin bot! Use the buttons below to navigate."
    await message.reply(start_text, reply_markup=keyboard)
