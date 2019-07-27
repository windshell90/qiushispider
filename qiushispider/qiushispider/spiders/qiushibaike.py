# -*- coding: utf-8 -*-
import scrapy
import time


class QiushibaikeSpider(scrapy.Spider):
    name = 'qiushibaike'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/']

    def parse(self, response):
        contents = response.xpath('//div[@id="content-left"]')
        selectors = contents.xpath('//div[contains(@class,"article block untagged")]')
        for selector in selectors:
            try:
                author = selector.xpath('./div/a/img/@alt').get()
                # author =selector.xpath('./div/a/h2/text()').get()
                gender_select = selector.xpath('./div/div[contains(@class,"articleGender")]/@class').get().split(' ')[-1]
                if gender_select == 'manIcon':
                    gender = '男'
                else:
                    gender = '女'
                age = selector.xpath('./div/div[contains(@class,"articleGender")]/text()').get()
                content = selector.xpath('.//a/div[@class="content"]/span/text()').get()
                with open('./qiushi.txt', 'a') as q:
                    q.write('作者：{}  性别：{}  年龄：{}  \n内容：{}\n\n\n'.format(author, gender, age, content))
            except:
                continue


        #翻页
        next_page = selector.xpath('//ul/li/a/span[@class="next"]/../@href').get()
        if next_page:
            next_url = response.urljoin(next_page)
            time.sleep(5)
            yield scrapy.Request(next_url, callback=self.parse)



