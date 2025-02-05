from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext
import logic
from config import TOKEN, DATABASE
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from logic import *
from config import *

bot = TeleBot(TOKEN)
# /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I'm a real estate bot. You can use commands to get information about a property. To get a list of commands type /help. Enjoy your use")


def help(update: Update, context: CallbackContext):
    help_text = (
        "Start working with the bot\n"
        "/help - List of commands\n"
        "/sale - Show properties for sale\n"
        "/transactions - Show recent transactions\n"
        "/city <name of the city> - Show properties in the specified city\n"
        "/agents - Show list of real estate agents"
    )
    update.message.reply_text(help_text)

# /sale command to display properties for sale
def sale(update: Update, context: CallbackContext):
    properties = logic.get_properties_for_sale()
    if properties:
        message = "Properties for sale:\n\n"
        for property in properties:
            message += f"Type: {property[0]}, \n Size: {property[1]} m², \n Price: {property[2]} $, \n Bedrooms: {property[3]}, \n Bathrooms: {property[4]}, \n City: {property[5]}, \n District: {property[6]}\n"
    else:
        message = "There are no properties for sale."
    update.message.reply_text(message)

# /transactions command to show latest transactions
def transactions(update: Update, context: CallbackContext):
    transactions = logic.get_transactions()
    if transactions:
        message = "Latest purchase deals:\n\n"
        for transaction in transactions:
            message += f"Client: {transaction[0]}, \n Property type: {transaction[1]}, \n Price: {transaction[2]} $, \n Date: {transaction[3]}\n"
    else:
        message = "No deals available"
    update.message.reply_text(message)

# /city command to search for real estate by city
def city(update: Update, context: CallbackContext):
    if context.args:
        city_name = " ".join(context.args)
        properties = logic.get_properties_in_city(city_name)
        if properties:
            message = f"Real estate in the city {city_name}:\n\n"
            for property in properties:
                message += f"Type: {property[0]}, \n Size: {property[1]} m², \n Price: {property[2]} $, \n Bedrooms: {property[3]}, \n Bathrooms: {property[4]}\n"
        else:
            message = f"No real estate in the city {city_name}."
    else:
        message = "Please indicate the city. Example: /city Moscow"
    update.message.reply_text(message)


def agents(update: Update, context: CallbackContext):
    agents = logic.get_agents()
    if agents:
        message = "List of real estate agents:\n\n"
        for agent in agents:
            message += f"Name: {agent[0]}, \n Phone: {agent[1]}, \n Email: {agent[2]} \n"
    else:
        message = "No agents available."
    update.message.reply_text(message)

def main():

    # Setting Up Updater and Dispatcher
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("sale", sale))
    dispatcher.add_handler(CommandHandler("transactions", transactions))
    dispatcher.add_handler(CommandHandler("city", city))
    dispatcher.add_handler(CommandHandler("agents", agents))

    # Bot launching
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
