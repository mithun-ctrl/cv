import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import MessageNotModified

logger = logging.getLogger(__name__)

# Callback handlers for the buttons
@Client.on_callback_query(filters.regex("^(about|home|help|support|back)$"))
async def button_callback(client, callback_query):
    try:
        data = callback_query.data
        logger.info(f"Button pressed: {data}")

        if data == "about":
            about_text = """
🤖 **Bot Information**
• Built with: Pyrogram
• Creator: Your Name
• Version: 1.0
• Purpose: Group Management
            """
            await callback_query.message.edit_text(about_text)
            
        elif data == "home":
            start_text = """
👋 Welcome to the Admin Bot!
Use the buttons below to navigate through various features.
            """
            await callback_query.message.edit_text(start_text, reply_markup=callback_query.message.reply_markup)
            
        elif data == "help":
            pin_button = InlineKeyboardButton("📌 Pin Commands", callback_data="pin")
            back_button = InlineKeyboardButton("🔙 Back", callback_data="back")
            help_keyboard = InlineKeyboardMarkup([[pin_button], [back_button]])
            help_text = """
📚 **Available Commands**
Select a category below to see specific commands.
            """
            await callback_query.message.edit_text(help_text, reply_markup=help_keyboard)
            
        elif data == "support":
            chat1_link = "https://t.me/your_chat1"
            chat2_link = "https://t.me/your_chat2"
            support_text = """
Need help? Join our support channels:
            """
            support_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Channel", url=chat1_link)],
                [InlineKeyboardButton("💭 Support Group", url=chat2_link)],
                [InlineKeyboardButton("🔙 Back", callback_data="back")]
            ])
            await callback_query.message.edit_text(support_text, reply_markup=support_keyboard)
            
        elif data == "back":
            keyboard = get_start_keyboard()
            start_text = """
👋 Welcome to the Admin Bot!
Use the buttons below to navigate through various features.
            """
            await callback_query.message.edit_text(start_text, reply_markup=keyboard)
            
    except MessageNotModified:
        pass
    except Exception as e:
        logger.error(f"Error in button callback: {str(e)}")
        await callback_query.answer("An error occurred. Please try again later.", show_alert=True)

def get_start_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
            InlineKeyboardButton("🏠 Home", callback_data="home")
        ],
        [
            InlineKeyboardButton("❔ Help", callback_data="help"),
            InlineKeyboardButton("📞 Support", callback_data="support")
        ]
    ])

# /start command
@Client.on_message(filters.command("start"))
async def start_command(client, message: Message):
    try:
        logger.info(f"Start command received from user {message.from_user.id}")
        keyboard = get_start_keyboard()
        start_text = """
👋 Welcome to the Admin Bot!
Use the buttons below to navigate through various features.
        """
        await message.reply(start_text, reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Error in start command: {str(e)}")
        await message.reply("An error occurred. Please try again later.")
