import pymongo
import json
from item import ItemList
from telebot import TelegramBot
import os

class LazadaScraperPipeline:

    collection_name = 'lazada_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=os.environ.get('MONGO_URI'),
            mongo_db=os.environ.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item['current_price'] != item['previous_price']:
            ItemList.update_last_price(item['item_id'], item['current_price'])
            self.db[self.collection_name].insert_one(dict(item))
            chat_ids = TelegramBot.getChatId()
            for chat_id in chat_ids:
                TelegramBot.sendMessage(chat_id, item)
        return item

