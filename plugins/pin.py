from pyrogram import Client, filters
from pyrogram.types import Message

from config import BOT_OWNER

# Helper function to check if a user is an admin or the group owner
async def is_admin_or_owner(message: Message):
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

# Callback handler for the "Pin" button
@Client.on_callback_query(filters.regex("^pin$"))
async def pin_button_callback(client, callback_query):
    pin_text = """
/pin - Silently pins the message that was replied to.
You can add the word 'loud' or 'notify' to the command to make the bot send a notification when pinning the message.

/unpin - Unpins the currently pinned message.

/pinned - Retrieves the currently pinned message and sends it back.
    """
    await callback_query.message.edit_text(pin_text)

# /pin command
@Client.on_message(filters.command("pin") & filters.group)
async def pin_message(client, message: Message):
    if not await is_admin_or_owner(message):
        return

    # Parse the optional 'loud' or 'notify' parameter
    is_loud = 'loud' in message.text.lower()
    is_notify = 'notify' in message.text.lower()

    # Pin the message
    await message.pin(disable_notification=not is_loud)

    # Send a notification if 'notify' is specified
    if is_notify:
        await message.reply("The message has been pinned.")

# /unpin command
@Client.on_message(filters.command("unpin") & filters.group)
async def unpin_message(client, message: Message):
    if not await is_admin_or_owner(message):
        return

    # Unpin the message
    await message.unpin()
    await message.reply("The pinned message has been unpinned.")

# /pinned command
@Client.on_message(filters.command("pinned") & filters.group)
async def get_pinned_message(client, message: Message):
    if not await is_admin_or_owner(message):
        return

    # Get the pinned message
    pinned_message = await message.chat.get_pinned_message()
    if pinned_message:
        await message.reply(f"The currently pinned message is:\n{pinned_message.text}")
    else:
        await message.reply("There is no pinned message in this chat.")
