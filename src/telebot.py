import requests
import json
import os

TOKEN = os.environ['TOKEN']
FLASK_URL = os.environ['FLASK_URL'] + '/handle_message'
BOT_API = "https://api.telegram.org/bot{}".format(TOKEN) 

class TelegramBot:
    def setWebhook():
        url = BOT_API + '/setWebhook?url=' + FLASK_URL
        requests.get(url)


    def setBotCommand():
        botcommands = [
            {
                "command": "/start",
                "description": "start using PriceTrackerBot"
            },
            {
                "command": "/add_item",
                "description": "<item url> <item name>"
            },
            {
                "command": "/get_all_item",
                "description": "get details of all items"
            },
            {
                "command": "/get_item_price",
                "description": "<item id>"
            },
            {
                "command": "/remove_item",
                "description": "<item id>"
            }, 
        ]
        botcommands = json.dumps(botcommands)
        url = BOT_API + '/setMyCommands?commands={}'.format(botcommands)
        requests.get(url)
    
    def getChatId():
        user = json.load(open('user.json','r'))
        return user
    
    def addChatId(chat_id):
        user = TelegramBot.getChatId()
        user.append(chat_id)
        f = open('user.json', 'w')
        f.write(json.dumps(user))

    def sendMessage(chat_id, message):
        url = BOT_API + '/sendMessage?chat_id={}&text={}'.format(chat_id, message)
        requests.get(url)

    