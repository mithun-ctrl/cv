import logging
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize the Pyrogram client
try:
    app = Client(
        "admin_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        in_memory=True  # Add this to prevent session file issues
    )
except Exception as e:
    logger.error(f"Error initializing client: {str(e)}")
    raise

# Import plugins after client initialization
try:
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
except Exception as e:
    logger.error(f"Error importing plugins: {str(e)}")
    raise

async def start_bot():
    try:
        await app.start()
        logger.info("Bot started successfully!")
        bot_info = await app.get_me()
        logger.info(f"Bot Username: @{bot_info.username}")
        
        # Register the commands and callbacks
        app.add_handler(pin_message)
        app.add_handler(unpin_message)
        app.add_handler(get_pinned_message)
        app.add_handler(pin_button_callback)
        app.add_handler(button_callback)
        app.add_handler(start_command)
        
        logger.info("All handlers registered successfully!")
        await idle()
    except Exception as e:
        logger.error(f"Error starting bot: {str(e)}")
        raise

if __name__ == "__main__":
    app.run(start_bot())
