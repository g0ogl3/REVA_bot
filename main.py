from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext
import logic
from config import TOKEN, DATABASE
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from logic import *
from config import *

bot = TeleBot(TOKEN)
# Команда /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я бот для работы с недвижимостью. Вы можете использовать команды для получения информации о недвижимости.")


def help(update: Update, context: CallbackContext):
    help_text = (
        "/start - Начать работу с ботом\n"
        "/help - Список команд\n"
        "/sale - Показать недвижимость в продаже\n"
        "/transactions - Показать последние сделки\n"
        "/city <город> - Показать недвижимость в указанном городе\n"
        "/agents - Показать список агентов недвижимости"
    )
    update.message.reply_text(help_text)

# Команда /sale для показа недвижимости в продаже
def sale(update: Update, context: CallbackContext):
    properties = logic.get_properties_for_sale()
    if properties:
        message = "Недвижимость в продаже:\n\n"
        for property in properties:
            message += f"Тип: {property[0]}, \n Размер: {property[1]} м², \n Цена: {property[2]} руб, \n Спальни: {property[3]}, \n Ванные: {property[4]}, \n Город: {property[5]}, \n Район: {property[6]}\n"
    else:
        message = "Нет недвижимости в продаже."
    update.message.reply_text(message)

# Команда /transactions для показа последних сделок
def transactions(update: Update, context: CallbackContext):
    transactions = logic.get_transactions()
    if transactions:
        message = "Последние сделки по покупке:\n\n"
        for transaction in transactions:
            message += f"Клиент: {transaction[0]}, \n Тип недвижимости: {transaction[1]}, \n Цена: {transaction[2]} руб, \n Дата: {transaction[3]}\n"
    else:
        message = "Нет доступных сделок."
    update.message.reply_text(message)

# Команда /city для поиска недвижимости по городу
def city(update: Update, context: CallbackContext):
    if context.args:
        city_name = " ".join(context.args)
        properties = logic.get_properties_in_city(city_name)
        if properties:
            message = f"Недвижимость в городе {city_name}:\n\n"
            for property in properties:
                message += f"Тип: {property[0]}, \n Размер: {property[1]} м², \n Цена: {property[2]} руб, \n Спальни: {property[3]}, \n Ванные: {property[4]}\n"
        else:
            message = f"Нет недвижимости в городе {city_name}."
    else:
        message = "Пожалуйста, укажите город. Пример: /city Москва"
    update.message.reply_text(message)


def agents(update: Update, context: CallbackContext):
    agents = logic.get_agents()
    if agents:
        message = "Список агентов недвижимости:\n\n"
        for agent in agents:
            message += f"Имя: {agent[0]}, \n Телефон: {agent[1]}, \n Email: {agent[2]} \n"
    else:
        message = "Нет доступных агентов."
    update.message.reply_text(message)

def main():

    # Настройка Updater и Dispatcher
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("sale", sale))
    dispatcher.add_handler(CommandHandler("transactions", transactions))
    dispatcher.add_handler(CommandHandler("city", city))
    dispatcher.add_handler(CommandHandler("agents", agents))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
