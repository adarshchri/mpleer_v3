import os
# importin the dotenv file to run the bot
from dotenv import load_dotenv
load_dotenv()

# defining the bot token
movie_token = os.getenv("MOVIE_TOKEN")
token = os.getenv("TOKEN")
