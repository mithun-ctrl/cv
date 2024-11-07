import os
import logging

logger = logging.getLogger(__name__)

try:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    BOT_OWNER = int(os.getenv("BOT_OWNER"))

    # Validate environment variables
    if not all([API_ID, API_HASH, BOT_TOKEN, BOT_OWNER]):
        raise ValueError("Missing required environment variables!")

except ValueError as e:
    logger.error(f"Environment variable error: {str(e)}")
    raise
except Exception as e:
    logger.error(f"Configuration error: {str(e)}")
    raise
