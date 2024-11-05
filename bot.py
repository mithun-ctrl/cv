import os
import random
import requests
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the token from the environment variable
TELEGRAM_BOT_TOKEN = os.getenv("TOKEN")

# AniList API query function to get a random anime frame
def fetch_random_frame():
    query = '''
    query ($page: Int, $perPage: Int) {
      Page(page: $page, perPage: $perPage) {
        media(type: ANIME, format: TV) {
          title {
            english
            romaji
          }
          coverImage {
            extraLarge
          }
          startDate {
            year
          }
          genres
        }
      }
    }
    '''
    variables = {
        'page': random.randint(1, 50),  # Random page to vary results
        'perPage': 1  # Get one anime per query for simplicity
    }

    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables})
    data = response.json()
    
    if 'errors' in data:
        return None
    
    anime = data['data']['Page']['media'][0]
    title = anime['title']['english'] or anime['title']['romaji']
    frame_url = anime['coverImage']['extraLarge']
    year = anime['startDate']['year']
    genre = ', '.join(anime['genres'])
    
    # Return structured frame data
    return {
        "title": title,
        "frame_url": frame_url,
        "year": year,
        "genre": genre
    }

# Asynchronous command handler to fetch and send an anime frame
async def post_frame(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    frame = fetch_random_frame()
    if frame:
        message = f"*Title*: {frame['title']}\n*Year*: {frame['year']}\n*Genre*: {frame['genre']}"
        await update.message.reply_photo(photo=frame['frame_url'], caption=message, parse_mode="Markdown")
    else:
        await update.message.reply_text("Failed to fetch frame. Please try again later.")

# Main function to set up the bot
async def main():
    if TELEGRAM_BOT_TOKEN is None:
        print("Error: TELEGRAM_BOT_TOKEN is not set in the .env file.")
        return

    # Create the Application instance with the bot token
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register the command handler for /post
    app.add_handler(CommandHandler("post", post_frame))

    # Start the bot
    print("Bot is starting...")
    await app.start()
    await app.updater.start_polling()
    await app.idle()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
