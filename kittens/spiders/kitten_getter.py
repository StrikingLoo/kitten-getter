import scrapy
import unicodedata
import requests
import re

def html_img_tag(img_url):
    return '<img width=\'30%\' height=\'30%\' src=\''+ img_url +'\' > </img><br/> '

def is_image(img_url):
    return img_url.endswith('.jpg') or img_url.endswith('.png') 

def get_image_urls(response):
    return [i.extract() for i in response.xpath('//a/@href') if is_image(i.extract()) ]

#must inherit from scrapy.Spider
class KittensSpider(scrapy.Spider):
    #can be any string, will be used to call from the console
    name = "kitten_getter"

    # This method must be in the spider, 
    # and will be automatically called by the crawl command.
    def start_requests(self):
        self.index = 0
        urls = [
            'http://reddit.com/r/cats',
        ]
        for url in urls:
            # We make a request to each url and call the parse function on the http response.
            yield scrapy.Request(url=url, callback=self.download_pictures)

    def make_html(self,response):
        final = '<script>var a = 5;</script>'
        image_urls = get_image_urls(response)
        for img_url in image_urls:
            final+= html_img_tag(img_url)
            print (img_url) 
        with open('links.html','a') as links:
            links.write(final)
        links.close()

    def download_pictures(self, response):
        image_urls = get_image_urls(response)
        for img_url in image_urls:
            self.index+=1
            print(img_url) 
            ascii_url = unicodedata.normalize('NFKD', img_url).encode('ascii','ignore')
            img_data = requests.get(ascii_url).content
            with open(str(self.index)+".jpg", 'w') as handler:
                handler.write(img_data)
