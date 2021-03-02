import scrapy

from scrapy.loader import ItemLoader
from ..items import BnpparibasplItem
from itemloaders.processors import TakeFirst


class BnpparibasplSpider(scrapy.Spider):
	name = 'bnpparibaspl'
	start_urls = ['https://media.bnpparibas.pl/informacje']

	def parse(self, response):
		post_links = response.xpath('//a[@class="button small"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//li[@class="arrow arrow--next"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="content-width"]//text()[normalize-space() and not(ancestor::h1 | ancestor::time)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//time/text()').get()

		item = ItemLoader(item=BnpparibasplItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
