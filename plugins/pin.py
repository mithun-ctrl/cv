import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import PinMessageError

from config import BOT_OWNER

logger = logging.getLogger(__name__)

# Helper function to check if a user is an admin or the group owner
async def is_admin_or_owner(message: Message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        
        # Check if the user is an admin
        status = await message.chat.get_member(user_id)
        if status.status in ["administrator", "creator"]:
            return True
        
        # Check if the user is the bot owner
        if user_id == int(BOT_OWNER):
            return True
        
        return False
    except Exception as e:
        logger.error(f"Error checking admin status: {str(e)}")
        return False

# Callback handler for the "Pin" button
@Client.on_callback_query(filters.regex("^pin$"))
async def pin_button_callback(client, callback_query):
    try:
        pin_text = """
📌 **Pin Commands**

• /pin - Silently pins the message
  Add 'loud' or 'notify' for notification

• /unpin - Unpins the current message

• /pinned - Shows the pinned message
        """
        await callback_query.message.edit_text(
            pin_text,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Back", callback_data="help")
            ]])
        )
    except Exception as e:
        logger.error(f"Error in pin button callback: {str(e)}")
        await callback_query.answer("An error occurred.", show_alert=True)

# /pin command
@Client.on_message(filters.command("pin") & filters.group)
async def pin_message(client, message: Message):
    try:
        if not message.reply_to_message:
            await message.reply("Please reply to a message to pin it!")
            return

        if not await is_admin_or_owner(message):
            await message.reply("You must be an admin to use this command!")
            return

        # Parse the optional 'loud' or 'notify' parameter
        is_loud = 'loud' in message.text.lower() or 'notify' in message.text.lower()

        # Pin the message
        await message.reply_to_message.pin(disable_notification=not is_loud)
        logger.info(f"Message pinned in chat {message.chat.id} by user {message.from_user.id}")

        if is_loud:
            await message.reply("Message has been pinned!")

    except PinMessageError as e:
        logger.error(f"Error pinning message: {str(e)}")
        await message.reply("Failed to pin message. Make sure I have the correct permissions.")
    except Exception as e:
        logger.error(f"Error in pin command: {str(e)}")
        await message.reply("An error occurred while pinning the message.")

# /unpin command
@Client.on_message(filters.command("unpin") & filters.group)
async def unpin_message(client, message: Message):
    try:
        if not await is_admin_or_owner(message):
            await message.reply("You must be an admin to use this command!")
            return

        # Unpin the message
        await client.unpin_chat_message(message.chat.id)
        logger.info(f"Message unpinned in chat {message.chat.id} by user {message.from_user.id}")
        await message.reply("Message has been unpinned!")

    except Exception as e:
        logger.error(f"Error in unpin command: {str(e)}")
        await message.reply("Failed to unpin message. Make sure I have the correct permissions.")

# /pinned command
@Client.on_message(filters.command("pinned") & filters.group)
async def get_pinned_message(client, message: Message):
    try:
        if not await is_admin_or_owner(message):
            await message.reply("You must be an admin to use this command!")
            return

        # Get the pinned message
        pinned_message = await message.chat.get_pinned_message()
        if pinned_message:
            await message.reply(f"📌 Currently pinned message:\n\n{pinned_message.text}")
        else:
            await message.reply("There are no pinned messages in this chat!")

    except Exception as e:
        logger.error(f"Error in pinned command: {str(e)}")
        await message.reply("An error occurred while fetching the pinned message.")
