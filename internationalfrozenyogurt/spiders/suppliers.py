import scrapy


class SuppliersSpider(scrapy.Spider):
    name = "suppliers"
    allowed_domains = ["internationalfrozenyogurt.com"]
    start_urls = ["https://internationalfrozenyogurt.com"]

    def parse(self, response):
        pass
