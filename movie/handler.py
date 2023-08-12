from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Update
from telegram.ext import ContextTypes
import base64
from movie.command import movie_search
from pagination_button import create_pagination_buttons
from movie.config import movie_server_list, movie_servers_config


async def movie_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    movie_data = query.data
    tmdb_id = movie_data.replace("movie_", "")
    keyboard = []

    for id, server in enumerate(movie_server_list):
        keyboard.append([
            InlineKeyboardButton(
                text=f"Server {id + 1}",
                callback_data=f"mserver_{server}_{tmdb_id}_{id + 1}"
            )
        ])
    movie_server_reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Select the Sever that you want to stream",
        reply_markup=movie_server_reply_markup,
    )


async def movie_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    movie_data = query.data.replace("mserver_", "").split('_')
    tmdb_id = movie_data[1]
    text = movie_data[2]

    link = movie_servers_config[movie_data[0]].format(tmdb_id)
    # Encode the argument_text to Base64
    string_to_encode = link
    encode_bytes = base64.b64encode(string_to_encode.encode("utf-8"))
    encoded_string = encode_bytes.decode("utf-8")

    streaming_link = f"https://mpleer.site/stream?movie={encoded_string }"

    message = (
        f"<b>Click Here to stream:</b> <a href='{streaming_link}'>Server {text}</a>"
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode="HTML",
        text=message,
    )

# Pagination Control


async def characters_page_callback(update, context=ContextTypes.DEFAULT_TYPE):

    character_pages = context.user_data.get("character_pages", [])
    query = update.callback_query
    print(query.data.split('_'))
    data_parts = query.data.split('_')
    print(data_parts)

    # if len(data_parts) == 2 and data_parts[0] == 'movie':
    #     character_id = data_parts[1]
    #     print(character_id)

    if len(data_parts) == 3 and data_parts[1] in ['prev', 'next']:
        action = data_parts[0]
        page = int(data_parts[2])
        total_pages = len(character_pages)

        print('callback', page)

        buttons = create_pagination_buttons(page, total_pages)

        # Define the current_character based on the current_page
        current_character = character_pages[page]

        stream_button_row = [
            InlineKeyboardButton(
                "Stream", callback_data=f"movie_{current_character['id']}")
        ]

        if page == 3:
            reply_markup = InlineKeyboardMarkup([buttons])
        else:

            reply_markup = InlineKeyboardMarkup([stream_button_row, buttons])

        message = current_character['message']

        await query.edit_message_media(
            media=InputMediaPhoto(
                media=current_character['poster'],
                caption=message,
                parse_mode='HTML'
            ),
            reply_markup=reply_markup,
        )

        await query.answer()  # Answer the callback query to remove the "loading" indicator

    else:
        await query.answer(text="Invalid action")
