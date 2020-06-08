import scrapy
from scrapy_splash import SplashRequest
from datetime import datetime
import pickle
import json
from item import ItemList

class LazadaWebScraper(scrapy.Spider):
    name='lazada_scraper'
    itemlist = ItemList.get_item()

    def start_requests(self):
        for item in self.itemlist:
            request = SplashRequest(url=item['item_url'], callback=self.parse, args={'wait': 3})
            request.cb_kwargs['item_id'] = item['item_id']
            request.cb_kwargs['item_url'] = item['item_url']
            request.cb_kwargs['item_name'] = item['item_name']
            request.cb_kwargs['last_price'] = item['last_price']
            yield request
    
    def parse(self, response, item_id, item_name, item_url, last_price):
        price =  response.xpath("//*[@id='module_product_price_1']/div/div/span/text()").get()
        price = price.replace("$", "")
        price = price.replace(",", "")

        is_buy_now = response.xpath('//*[@id="module_add_to_cart"]/div/button[1]/span/span/text()').get()
        availability = 'Available' if is_buy_now == "Buy Now" else "Out of Stock"
        
        item = {
            "item_id": item_id,
            "item_url": item_url,
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "item_name": item_name,
            "current_price": float(price),
            "previous_price": last_price,
            "availability":availability
        }
        yield item