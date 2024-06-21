import scrapy
from scrapy.http import TextResponse
from bs4 import BeautifulSoup


class SuppliersSpider(scrapy.Spider):
    name = "suppliers"
    allowed_domains = ["internationalfrozenyogurt.com"]
    start_urls = ["https://internationalfrozenyogurt.com/suppliers/"]

    def parse(self, response):
        next_page_url = response.xpath('//li[@class="bpn-next-link"]/a/@href').get()
        if next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse)

        # some bug with the response.xpath('//article') is happening
        suppliers_container = BeautifulSoup(response.body, 'html.parser').find_all('article')

        for container in suppliers_container:
            container = TextResponse(url=response.url, body=str(container), encoding='utf-8')

            address = container.xpath('.//div[@class="contact-item supplier-address"]/text()').getall()
            if address:
                address = ','.join([line.strip() for line in address if line.strip() != ''])

            phone = container.xpath('.//div[@class="contact-item supplier-phone"]/text()').get()
            if phone:
                phone = phone.strip()

            supplier = {
                'name': container.xpath('.//h3/a/text()').get(),
                'url': container.xpath('.//h3/a/@href').get(),
                'categories': container.xpath('.//div[@class="supplier-categories"]/span/a/text()').getall(),
                'website': container.xpath('.//div[@class="contact-item supplier-website"]/a/@href').get(),
                'phone': phone,
                'address': address,
            }
            yield supplier


