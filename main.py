from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

from plugins.pin import (
    pin_message,
    unpin_message,
    get_pinned_message,
    pin_button_callback
)
from plugins.button import (
    button_callback,
    start_command
)

# Initialize the Pyrogram client
app = Client("admin_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Register the commands and callbacks
app.add_handler(pin_message)
app.add_handler(unpin_message)
app.add_handler(get_pinned_message)
app.add_handler(pin_button_callback)
app.add_handler(button_callback)
app.add_handler(start_command)

# Run the bot
app.run()
