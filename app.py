from routes import routes, commands
from api_token import token, url, port
import base64
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
)

from dotenv import load_dotenv
load_dotenv()

# from movie_server import movie_vidsrc
logging.basicConfig(
    filename="app.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


# Welcome Text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_url = "https://postimg.cc/7JMQrS1D"
    greeting = f"Hiii!!🤩 {update.effective_user.first_name}"
    header = "🍿 Welcome to the worlds largest search engine on the net!"
    paragraph = "Here, you can watch any movie/series by just typing name of a film or series..🔍"
    example = "<b>E.g /tmdb 132117 </b>\n <b>E.g /movie pathaan </b> \n <b>E.g /tv farzi </b> \n"
    instructions = "⚠️ 𝖧𝗂𝗍 Help for watch video about How to search/watch...❓"
    browser = "🏹 Use Brave Browser on Mobile or Computer to Block Ads"
    maker = "❤️ Powered by: @mpleer_bot"
    keyboard = [
        [
            InlineKeyboardButton(
                text="🤖 Update", url="https://t.me/mpleer_group"),
            InlineKeyboardButton(
                text="🎬 MPleer Network", url="https://t.me/mpleer_networks"
            ),
        ],
        [
            InlineKeyboardButton(
                text="📣 Feedback",
                url="https://t.me/mpleer_feedback",
            ),
            InlineKeyboardButton(
                text="ℹ️ Help",
                url="https://www.youtube.com/watch?v=vZtm1wuA2yc&ab_channel=Indently",
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = f"{greeting} \n\n<b>{header}</b> \n\n {paragraph} \n\n {example} \n\n {instructions} \n\n <b> {browser} </b> \n\n\n <b> {maker}</b>\n"
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=photo_url,
        caption=message,
        reply_markup=reply_markup,
        parse_mode="HTML",
    )


# Search movie by name


if __name__ == "__main__":

    application = ApplicationBuilder().token(token).build()

    # Start Handler
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    for command in commands:
        application.add_handler(CommandHandler(
            command.get('command'), command.get('func')))

    # # Tv
    # tv_handler = CommandHandler("tv", tv_search)
    # application.add_handler(tv_handler)

    for route in routes:
        handler = CallbackQueryHandler(route.get('func'), route.get('path'))
        application.add_handler(handler)

    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=token,
        webhook_url=f"{url}/{token}",
    )
    # application.run_polling()
