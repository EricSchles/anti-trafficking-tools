import scrapy
import IPython
from app.models import BackpageAdInfo
from app import db
from datetime import datetime

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
			 url = ad.root
			 phone_number,post_id = url.split("/")[-2:]
			 title = phone_number
			 ad_obj = BackpageAdInfo(
			 	url,
				title,
				phone_number,
				"", #location
				"", #latitude
				"", #longitude
				"",	#ad_body
				"", #photos
				post_id, #post_id
				datetime.now(), #timestamp
				"", #city
				"", #state
			 )
			 db.session.add(ad_obj)
			 db.session.commit()
