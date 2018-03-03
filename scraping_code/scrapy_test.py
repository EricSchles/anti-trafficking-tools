import scrapy 
import IPython

class BlogSpider(scrapy.Spider):
	name = "backpage_spider"
	start_urls = [
	"http://manhattan.backpage.com/WomenSeekMen/",
	"http://manhattan.backpage.com/MenSeekWomen/",
	"http://manhattan.backpage.com/MenSeekMen/",
	"http://manhattan.backpage.com/WomenSeekWomen/",
	"http://manhattan.backpage.com/Transgender/"
	]

	def parse(self, response):
		for ad in response.xpath("//div[contains(@class, 'cat')]/a/@href"):
			yield {"ad": ad.root}
