import json
import os.path

JSON_PATH = './item.json'

class ItemList:
    def __init__(self):
        self.counter = 1

    def get_item(item_id=None):
        itemlist = json.load(open(JSON_PATH, 'r'))
        print(itemlist)
        if item_id is None:
            return itemlist
        else:
            for item in itemlist:
                if item['item_id'] == item_id:
                    return item

    def write_to_json_file(itemlist):
        f = open(JSON_PATH, 'w')
        f.write(json.dumps(itemlist))
                   
    def add_item(self,item_name, item_url):
        itemlist = ItemList.get_item()
        item = {
            "item_id": self.counter,
            "item_name": item_name,
            "item_url": item_url, 
            "last_price": 0
        }
        itemlist.append(item)
        self.counter += 1
        ItemList.write_to_json_file(itemlist)
        return "item added"
    
    def remove_item(self,item_id):
        itemlist = ItemList.get_item()
        for i in range(len(itemlist)):
            if item_id == itemlist[i]['item_id']:
                del itemlist[i]
                break
        else:
            return "item id not found"
                    
        ItemList.write_to_json_file(itemlist)
        return "item removed"

    def update_last_price(item_id, last_price):
        itemlist = ItemList.get_item()
        for item in itemlist:
            if item_id == item['item_id']: 
                item['last_price'] = last_price
                break
        else:
            return "item id not found"

        ItemList.write_to_json_file(itemlist)
        return "item price updated"
