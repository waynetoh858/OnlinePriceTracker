import subprocess

def scrape():
    subprocess.call('scrapy crawl lazada_scraper', shell=True)

class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': scrape,
            'trigger': 'interval',
            'seconds': 60
        }
    ]

    SCHEDULER_API_ENABLED = True