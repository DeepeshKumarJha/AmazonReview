import sys
from os import system
from scrapy.crawler import CrawlerProcess
from amazonReview.spiders.review import ReviewSpider

system('clear')

if '-l' in sys.argv:

    index = sys.argv.index('-l')

    try:
        if sys.argv[index+1]:
            urls = sys.argv[index+1:]
    except:
        print("PLEASE PROVIDE LINKS AFTER '-l' ")
        exit()

    print("Extracting Reviews, Please Wait ................")

else:
    print("Provide the product page link like: run.py -l <link>, <link>,...")
    exit()

reviewProcess = CrawlerProcess(
    settings={
        'LOG_LEVEL': 'WARNING',
        "FEEDS": {
            "items.csv": {
                "format": "csv",
            },
        },
    }
)

reviewProcess.crawl(ReviewSpider, urls=urls)

reviewProcess.start()
