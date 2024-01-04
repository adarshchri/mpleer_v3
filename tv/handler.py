from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from api_token import movie_token
import requests
from .config import tv_server_list, tv_servers_config

import base64


async def tv_season(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    tmdb_id = query.data.replace("tv_", "")

    tv_season_url = f"https://api.themoviedb.org/3/tv/{tmdb_id}?api_key={movie_token}&external_source=imdb_id"
    tv_season_response = requests.get(tv_season_url)
    tv_seasons = tv_season_response.json().get("seasons")
    context.user_data["tmdb_id"] = tmdb_id

    keybord = []

    for season in tv_seasons:
        keybord.append(
            [
                InlineKeyboardButton(
                    text=f"Season {season.get('season_number')}",
                    callback_data=f"season_-{season.get('season_number')}-_episodes_-{season.get('episode_count')}",
                )
            ]
        )
    reply_markup = InlineKeyboardMarkup(keybord)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Select Season",
        reply_markup=reply_markup,
    )


async def tv_servers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    state = query.data.split("-")

    print(state)

    seasons = int(state[1].strip())
    episodes = int(state[3].strip())

    context.user_data["seasons"] = seasons
    context.user_data["episodes"] = episodes

    keyboard = []

    for id, server in enumerate(tv_server_list):
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"Server {id + 1}", callback_data=f"tserver_{server}_{id+1}"
                )
            ]
        )
    tv_server_reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Select the Sever that you want to stream \n<b>Use Brave Browser to block ads.</b>",
        reply_markup=tv_server_reply_markup,
        parse_mode="HTML",
    )


async def tv_episodes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data_part = query.data.replace("tserver_", "").split("_")
    print(data_part)
    server = data_part[0]
    text = data_part[1]
    seasons = context.user_data.get("seasons", None)
    episodes = context.user_data.get("episodes", None)
    tmdb_id = context.user_data.get("tmdb_id", None)

    links = []
    for episode_number in range(1, episodes + 1):
        link = tv_servers_config.get(server).format(
            tmdb_id, seasons, episode_number)
        # Encode the link in Base64
        string_to_encode = link
        encode_bytes = base64.b64encode(string_to_encode.encode("utf-8"))
        encoded_string = encode_bytes.decode("utf-8")
        # Create a clickable link using Markdown formatting
        clickable_link = f"<b>Episode {episode_number}</b> : <a href='https://mpleer.onrender.com/stream?movie={encoded_string}'>Click here to stream</a>"
        links.append(clickable_link)

    # Now 'links' list contains the clickable links for all episodes in the selected season
    link_text = "\n".join(links)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Season is: {seasons}\nTotal episodes: {episodes}\nServer: {text}\nLinks:\n{link_text}",
        parse_mode="HTML",
    )
