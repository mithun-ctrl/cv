import os
from telegram.ext import Updater, CommandHandler
from jikanpy import Jikan
from dotenv import load_dotenv
load_dotenv()

# Replace 'YOUR_BOT_TOKEN' with the API token provided by the BotFather
BOT_TOKEN = 'TOKEN'

# Initialize the Jikan API client
jikan = Jikan()

# Keep track of posted characters
posted_characters = []

def post_anime_character(update, context):
    """
    Handles the /post command to post a random anime character image.
    """
    # Fetch a random anime character from the Jikan API
    character = jikan.random_character()['data']

    # Check if the character has been posted before
    if character['mal_id'] in posted_characters:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I can't post the same character again!")
        return

    # Post the character's image
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=character['image_url'])

    # Add the character to the posted_characters list
    posted_characters.append(character['mal_id'])

    # Limit the list to the last 100 posted characters
    if len(posted_characters) > 100:
        posted_characters.pop(0)

def main():
    """
    Main function to set up and run the Telegram bot.
    """
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register the /post command handler
    dispatcher.add_handler(CommandHandler('post', post_anime_character))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
