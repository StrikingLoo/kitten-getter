import scrapy


def html_img_tag(img_url):
    return '<img width=\'30%\' height=\'30%\' src=\''+ img_url +'\' > </img><br/> '

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
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        final = '<script>var a = 5;</script>'
        for i in response.xpath('//a/@href'):
            img_url = i.extract()
            if img_url.endswith('.jpg') or img_url.endswith('.png'):
                final+= html_img_tag(img_url)
                print (img_url) 
        with open('links.html','a') as links:
            links.write(final)
        links.close()
        '''print('all is right')
        nextLink = response.css('span.next-button a::attr(href)')[0].extract()
        print(nextLink)
        self.count += 1
        if self.count<10:
            yield scrapy.Request(url = nextLink,callback = self.parse)'''
