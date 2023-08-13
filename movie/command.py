from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import base64
import requests
import datetime

from api_token import movie_token

from pagination_button import create_pagination_buttons

from utils import download_file


async def movie_tmdb_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    argument = context.args
    argument_text = " ".join(argument)
    context.user_data["argument_text"] = argument_text

    base_url = f"https://api.themoviedb.org/3/movie/{argument_text}?api_key={movie_token}&external_source=imdb_id"
    movie_detail = requests.get(base_url).json()

    if "id" in movie_detail:
        # Getting title becaue tmdb have different variable decleration for movie
        id = movie_detail["id"]
        context.user_data["id"] = id
        title = movie_detail["title"]
        original_title = movie_detail["original_title"]
        # overview = movie_detail["overview"]
        poster_path = movie_detail["poster_path"]
        genre = [genre["name"] for genre in movie_detail["genres"]]
        genre_string = ", ".join(genre)
        release_date = movie_detail["release_date"]
        formatted_release_date = datetime.datetime.strptime(
            release_date, "%Y-%m-%d"
        ).strftime("%d-%m-%Y")
        vote = movie_detail["vote_average"]
        trailer = (
            f"https://api.themoviedb.org/3/movie/{id}/videos?api_key={movie_token}"
        )
        trailer_response = requests.get(trailer).json()
        # Set a default value for key
        key = None
        for trailer_result in trailer_response["results"]:
            if trailer_result["site"].lower() == "youtube":
                key = trailer_result["key"]

        if key:
            trailer_key = key
            trailer_link = f"https://www.youtube.com/watch?v={trailer_key}"
            message = f"<b>{title}</b>\n\nGenres: {genre_string}\n\n<b>Release Date:</b> {formatted_release_date}\n\n<b>Trailer:</b> <a href='{trailer_link}'>Watch Now</a>"
        else:
            message = f"<b>{title}</b>\n\nGenres: {genre_string}\n\n<b>Release Date:</b> {formatted_release_date}\n\n<b>Trailer:</b> Trailer not available."

        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            poster_url = "https://i.postimg.cc/cLGBr4Ry/carbon.png"

        keybord = [
            [InlineKeyboardButton(
                text="Stream", callback_data=f"movie_{id}")]
        ]
        reply_makup = InlineKeyboardMarkup(keybord)

        file = download_file(poster_url)
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            parse_mode="HTML",
            photo=file,
            reply_markup=reply_makup,
            caption=message,
        )

        # await movie_checker(update, context)


# pagination movie

async def movie_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    character_pages = []
    context.user_data['character_pages'] = character_pages

    argument = context.args
    if not argument:
        movie_not_found = "<b>Type /movie &lt;Series Name&gt; </b> \n <b>E.g /movie pathaan</b>"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=movie_not_found,
            parse_mode='HTML'
        )
        return
    search_result = await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Processing ...."
    )
    argument_text = " ".join(argument)
    context.user_data["argument_text"] = argument_text

    base_url = f"https://api.themoviedb.org/3/search/movie?query={argument_text}&api_key={movie_token}&include_adult=false&language=en-US&page=1"
    movie_details = requests.get(base_url).json()

    genre_url = f"https://api.themoviedb.org/3/genre/movie/list?language=en&api_key={movie_token}"
    genre_response = requests.get(genre_url).json()
    genre_mapping = {genre['id']: genre['name']
                     for genre in genre_response['genres']}

    if len(movie_details['results']) > 0:
        for movie_detail in movie_details['results']:
            id = movie_detail["id"]
            title = movie_detail["title"]
            original_title = movie_detail["original_title"]
            # overview = movie_detail["overview"]
            # max_chars = 50  # Approximate number of characters for two lines
            # truncated_overview = overview[:max_chars].strip()

            # if len(overview) > max_chars:
            #     truncated_overview += " ..."  # Add ellipsis if truncated
            poster_path = movie_detail["poster_path"]
            genre_ids = movie_detail['genre_ids']
            genre_names = [genre_mapping.get(genre_id, '')
                           for genre_id in genre_ids]
            genre_string = ", ".join(genre_names)
            release_date = movie_detail["release_date"]
            if release_date:
                formatted_release_date = datetime.datetime.strptime(
                    release_date, "%Y-%m-%d"
                ).strftime("%d-%m-%Y")
                keybord = [
                    [InlineKeyboardButton(
                        text="Stream", callback_data=f"movie_{id}")]
                ]
                reply_makup = InlineKeyboardMarkup(keybord)
            else:
                # Skip movies without a release date
                continue

            vote = movie_detail["vote_average"]
            trailer = f"https://api.themoviedb.org/3/movie/{id}/videos?api_key={movie_token}"
            trailer_response = requests.get(trailer).json()
            # Set a default value for key
            key = None
            for trailer_result in trailer_response["results"]:
                if trailer_result["site"].lower() == "youtube":
                    key = trailer_result["key"]
            if key:
                trailer_key = key
                trailer_link = f"https://www.youtube.com/watch?v={trailer_key}"
                message = f"<b>{title}</b>\n\n<b>Genres:</b> {genre_string}\n\n<b>Release Date:</b> {formatted_release_date}\n\n<b>Trailer:</b> <a href='{trailer_link}'>Watch Now</a>"
            else:
                message = f"<b>{title}</b>\n\n<b>Genres:</b> {genre_string}\n\n<b>Release Date:</b> {formatted_release_date}\n\n<b>Trailer:</b> Trailer not available."

            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            else:
                poster_url = "https://i.postimg.cc/cLGBr4Ry/carbon.png"

            character_pages.append(
                {
                    'id': id,
                    'message': message,
                    'poster': poster_url
                }
            )
        # Inserted the Extra Page for the Tmdb notice
        if len(character_pages) >= 3:
            extra_page = {
                'title': 'tmdb',
                'message': '<b>How to Search Movie if You Not able to Find in the Slide</b>\n\n\n\n<b>Just Get the TMDB id of movie Which you want to watch</b>\n\n<b>And Type</b>\n\n<b>/tmdb tmdb_id</b>',
                'poster': 'https://i.postimg.cc/cL3kbbmZ/tmdb-image.png',
                'id': '4'
            }
            character_pages.insert(3, extra_page)

        # Define the current_page and the total_page and call the button function
        current_page = 0
        total_pages = len(character_pages)
        buttons = create_pagination_buttons(current_page, total_pages)

        # Define the current_character based on the current_page
        current_character = character_pages[current_page]

        # Create a separate row for the "Stream" button
        stream_button_row = [
            InlineKeyboardButton(
                "Stream", callback_data=f"movie_{current_character['id']}")
        ]

        # Combine the buttons and the stream_button_row into the reply_markup
        reply_markup = InlineKeyboardMarkup([stream_button_row, buttons])

        message = current_character['message']

        file = download_file(current_character['poster'])
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=file,
            caption=message,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Movie Not Found. Check the Spell"
        )
