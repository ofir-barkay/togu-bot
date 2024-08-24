from dotenv import load_dotenv
import os
import html
import json
import traceback
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
from telegram.constants import ParseMode
import functools

load_dotenv('.env')
from TourGuideAgency.agency import init_agency

async def unauthorised(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Unauthorized User')

def require_auth():
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args):
            update = args[0]
            if update.effective_user.id == int(os.getenv('AUTH_TELEGRAM_USER_ID')):
                return await func(*args)
            else:
                return await unauthorised(*args)
        return wrapped
    return wrapper

@require_auth()
async def prompt_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Do you want to start?', reply_markup=ReplyKeyboardMarkup([[KeyboardButton('/start')]], one_time_keyboard=True))


AWAIT_LOCATION, RELAY_AGENT = 1, 2

@require_auth()
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    agency = init_agency()
    context.bot_data.update({'agency':agency})
    await update.message.reply_text(f'Hello! Im ToGu - Your AI Tour Guide 🌍🌎🌏')
    location_button = KeyboardButton(text="Share Location", request_location=True)
    location_reply_markup = ReplyKeyboardMarkup([[location_button]], one_time_keyboard=True)
    await update.message.reply_text('Lets start by sharing your current location 📍', reply_markup=location_reply_markup)

    return AWAIT_LOCATION



async def get_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_location = update.message.location
    latitude = user_location.latitude
    longitude = user_location.longitude
    context.user_data.update({'longitude': longitude, 'latitude': latitude})
    agency = context.bot_data.get('agency')
    response = agency.get_completion(f'Hi, im currently at longitude:{longitude} ; latitude:{latitude}')
    await update.message.reply_text(response)

    return RELAY_AGENT

async def relay(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    agency = context.bot_data.get('agency')
    response = agency.get_completion(message=update.message.text, verbose=True)
    await update.message.reply_markdown(response)

    if agency.shared_state.get('finished') == True:
        agency = context.bot_data.get('agency')
        agency.delete()

        return ConversationHandler.END

    return RELAY_AGENT

async def abort(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.bot_data.get('agency').delete()
    await update.message.reply_text('aborted, ready to start over')


async def error_handler(update: object, context:ContextTypes.DEFAULT_TYPE):
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error("Exception while handling an update:", exc_info=context.error)
    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)
    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = ''.join([
        "An exception was raised while handling an update\n",
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}",
        "</pre>\n\n",
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n",
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n",
        f"<pre>{html.escape(tb_string)}</pre>"
    ])
    await update.message.reply_text(text=message[:4096], parse_mode=ParseMode.HTML)


if __name__ == '__main__':
    load_dotenv('.env')
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)
    conversation  = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AWAIT_LOCATION: [MessageHandler(filters.LOCATION, get_location)],
            RELAY_AGENT: [MessageHandler(filters.TEXT, relay)]
        },
        fallbacks=[CommandHandler('abort', abort)]
    )
    app = ApplicationBuilder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
    app.add_handler(conversation)
    app.add_handler(MessageHandler(filters.TEXT, prompt_start))
    app.add_error_handler(error_handler)
    app.run_polling(allowed_updates=Update.ALL_TYPES)
