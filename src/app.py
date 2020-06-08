from flask import Flask, request
from flask_apscheduler import APScheduler
from scheduler import Config
from item import ItemList
from telebot import TelegramBot
import json
import requests

app = Flask(__name__)

# scheduler
app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# item.json
itemlist = ItemList()

# telebot
TelegramBot.setWebhook()
TelegramBot.setBotCommand()

@app.route('/handle_message', methods=['POST'])
def handle_message():
    incoming_message = request.json
    chat_id = incoming_message['message']['chat']['id']
    command = incoming_message['message']['text'].split()

    if '/start' == command[0]:
        TelegramBot.addChatId(chat_id)
        outgoing_message = 'Hi there! How may I help you?'

    elif '/get_all_item' == command[0]:
        item_list = ItemList.get_item()
        for item in item_list:
            outgoing_message = "Item ID:\t{}\nItem Name:\t{}\nMost Recent Price:\t{}\n".format(item['item_id'], item['item_name'], item['last_price'])
            TelegramBot.sendMessage(chat_id, outgoing_message)
        return "Message Sent"

    elif '/get_item_price' == command[0]:
        try:
            item_id = int(command[1])
            outgoing_message = ItemList.get_item(item_id)
        except:
            outgoing_message = "invalid item id"

    elif '/remove_item' == command[0]:
        try:
            item_id = int(command[1])
            outgoing_message = itemlist.remove_item(item_id)
        except:
            outgoing_message = "invalid item id"

    elif '/add_item' == command[0]:
        try:
            if requests.get(command[1]).status_code != 200:
                outgoing_message = "status code not 200"
            elif len(command) <= 2:
                outgoing_message = "Please enter an item name"
            else:
                outgoing_message = itemlist.add_item(' '.join(command[2:]), command[1])
        except:
            outgoing_message = "invalid url"

    else:
        outgoing_message = "invalid bot command"

    TelegramBot.sendMessage(chat_id, outgoing_message)
    return "Message Sent"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)