
import scrapy
class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://blog.cyble.com',
    ]

    def parse(self, response):
        for quote in response.css('div.uael-post-wrapper'):
            yield {
                #'author': quote.xpath('span/small/text()').get(),
                'url': quote.css('div a::attr("href")').get(),
            }
            #print(quote.css('div a::attr("href")').get())
        # div.uael-post__body > div > div > div > div > a::attr("href")
        next_page = response.css('div.uael-post__footer > nav > a.next::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
