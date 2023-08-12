from telegram import Update
from telegram.ext import ContextTypes

from movie.command import movie_tmdb_search
from tv.command import tv_tmdb_search


async def tmdb_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    search_result = await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Processing ...."
    )
    # Call the movie_tmdb_search function first
    await movie_tmdb_search(update, context)

    # Check if data was found in tmdb_search
    if "id" not in context.user_data:
        # Call the tv_tmdb_search function if data was not found in tmdb_search
        await tv_tmdb_search(update, context)
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Movie not found.",
        )

    # # If data is still not found, send "Movie not found" message
    # if "id" not in context.user_data:
    #     print('ya that me')
    #     await context.bot.send_message(
    #         chat_id=update.effective_chat.id,
    #         text="Movie not found.",
    #     )
