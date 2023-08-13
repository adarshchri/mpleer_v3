from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import base64
import requests
import datetime

from api_token import movie_token
from pagination_button import create_pagination_buttons


async def tv_tmdb_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    argument = context.args
    argument_text = " ".join(argument)
    context.user_data["argument_text"] = argument_text

    base_url = f"https://api.themoviedb.org/3/tv/{argument_text}?api_key={movie_token}&external_source=imdb_id"
    tv_detail = requests.get(base_url).json()

    if "id" in tv_detail:
        id = tv_detail["id"]
        context.user_data["id"] = id
        title = tv_detail["name"]
        original_name = tv_detail["original_name"]
        # overview = tv_detail["overview"]
        poster_path = tv_detail["poster_path"]
        genre = [genre["name"] for genre in tv_detail["genres"]]
        genre_string = ", ".join(genre)
        release_date = tv_detail["first_air_date"]
        formatted_release_date = datetime.datetime.strptime(
            release_date, "%Y-%m-%d"
        ).strftime("%d-%m-%Y")
        vote = tv_detail["vote_average"]
        season = [
            {
                "season_number": season["season_number"],
                "episode_count": season["episode_count"],
            }
            for season in tv_detail["seasons"]
            if season["air_date"] is not None
        ]
        # Create a string with season numbers and release dates
        # Assuming you already have the 'season' list as you mentioned in your previous code.
        season_strings = [
            f"Season {season['season_number']}" for season in season]

        # Convert the list of season strings into a comma-separated string
        season_string = ", ".join(season_strings)
        trailer = (
            f"https://api.themoviedb.org/3/tv/{id}/videos?api_key={movie_token}"
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
            message = f"<b>{title}</b>\n\nGenres: {genre_string}\n\n<b>Seasons:</b> {season_string}\n\n<b>Release Date:</b> {formatted_release_date}\n\n<b>Trailer:</b> <a href='{trailer_link}'>Watch Now</a>"
        else:
            message = f"<b>{title}</b>\n\nGenres: {genre_string}\n\n<b>Seasons:</b> {season_string}\n\n<b>Release Date:</b> {formatted_release_date}\n\n<b>Trailer:</b> Trailer not available."

        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"

        keybord = [
            [InlineKeyboardButton(
                text="Stream", callback_data=f"tv_{id}")]
        ]
        reply_makup = InlineKeyboardMarkup(keybord)

        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            parse_mode="HTML",
            photo=poster_url,
            reply_markup=reply_makup,
            caption=message,
        )

# Tv Search Pagination


async def tv_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    character_pages = []
    context.user_data['character_pages'] = character_pages

    argument = context.args

    if not argument:
        tv_not_found = "<b>Type /tv &lt;Series Name&gt; </b> \n <b>E.g /tv farzi</b>"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=tv_not_found,
            parse_mode='HTML'
        )
        return
    search_result = await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Processing ...."
    )
    argument_text = " ".join(argument)
    context.user_data["argument_text"] = argument_text

    base_url = f"https://api.themoviedb.org/3/search/tv?query={argument_text}&api_key={movie_token}&include_adult=false&language=en-US&page=1"
    movie_details = requests.get(base_url).json()

    genre_url = f"https://api.themoviedb.org/3/genre/tv/list?language=en&api_key={movie_token}"
    genre_response = requests.get(genre_url).json()
    genre_mapping = {genre['id']: genre['name']
                     for genre in genre_response['genres']}
    if len(movie_details['results']) > 0:
        for movie_detail in movie_details['results']:
            id = movie_detail["id"]
            title = movie_detail["name"]
            original_title = movie_detail["original_name"]
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
            release_date = movie_detail["first_air_date"]
            if release_date:
                formatted_release_date = datetime.datetime.strptime(
                    release_date, "%Y-%m-%d"
                ).strftime("%d-%m-%Y")
                keybord = [
                    [InlineKeyboardButton(
                        text="Stream", callback_data=f"tv_{id}")]
                ]
                reply_makup = InlineKeyboardMarkup(keybord)
            else:
                # Skip movies without a release date
                continue

            vote = movie_detail["vote_average"]
            trailer = f"https://api.themoviedb.org/3/tv/{id}/videos?api_key={movie_token}"
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
                poster_url = "https://postimg.cc/K4qVpHk2"

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
                'message': '<b>How to Search Series if You Not able to Find in the Slide</b>\n\n\n\n<b>Just Get the TMDB id of movie Which you want to watch</b>\n\n<b>And Type</b>\n\n<b>/tmdb tmdb_id</b>',
                'poster': 'https://postimg.cc/ykJfw5DS',
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
                "Stream", callback_data=f"tv_{current_character['id']}")
        ]

        # Combine the buttons and the stream_button_row into the reply_markup
        reply_markup = InlineKeyboardMarkup([stream_button_row, buttons])

        message = current_character['message']

        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=current_character['poster'],
            caption=message,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Series Not Found. Check the Spell"
        )
