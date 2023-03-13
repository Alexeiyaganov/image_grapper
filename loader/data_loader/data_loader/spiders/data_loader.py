import scrapy
import os
from data_loader.items import DataLoaderItem

i = 0


class RalphLaurenSpider(scrapy.Spider):
    name = 'data_loader'
    start_urls = [
        'https://www.ralphlauren.com/en/men/clothing/hoodies-sweatshirts/10204?webcat=men%7Cclothing%7Cmen-clothing-hoodies-sweatshirts']
    allowed_domains = ['ralphlauren.com']

    def parse(self, response):
        links = response.css('a.thumb-link::attr(href)').getall()

        # scrape all the images in a loop
        for item in links:
            yield scrapy.Request('https://www.ralphlauren.com' + item, self.parse_cloth)

        next_page = response.css('div.pagination-flex a::attr(href)').get()
        if next_page:
            yield scrapy.Request(next_page, self.parse)

    def parse_cloth(self, response):
        images = response.css('div.swiper-wrapper.main-images')
        # image urls
        person_image_urls = images.css('div[data-slideindex="0"] picture::attr(data-highres-images)').getall()
        cloth_image_urls = images.css('div[data-slideindex="1"] picture::attr(data-highres-images)').getall()
        image_urls = [person_image_urls, cloth_image_urls]

        for img_type in image_urls:
            for url in img_type:
                global i
                item = DataLoaderItem()
                item['image_urls'] = [url]
                if img_type is person_image_urls:
                    str_img_type = 'person'
                    i += 1
                if img_type is cloth_image_urls: str_img_type = 'cloth'
                item['image_type'] = os.path.join(f"{str_img_type}", f"{i}.jpg")
                yield item
