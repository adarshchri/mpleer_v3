import os
# importin the dotenv file to run the bot
from dotenv import load_dotenv
load_dotenv()

# defining the bot token
port = os.getenv("PORT")
url = os.getenv("URL")
movie_token = os.getenv("MOVIE_TOKEN")
token = os.getenv("TOKEN")
