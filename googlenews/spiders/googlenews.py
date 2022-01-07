import scrapy
from scrapy.http.response.html import HtmlResponse
class GoogleNewsSpider(scrapy.Spider):
    name = "googlenews"
    start_urls = [
        'https://news.google.com/topics/CAAqLAgKIiZDQkFTRmdvSUwyMHZNRFZxYUdjU0JtVnpMVFF4T1JvQ1EwOG9BQVAB?hl=es-419&gl=CO&ceid=CO%3Aes-419',
        # 'https://news.google.com/topics/CAAqLAgKIiZDQkFTRmdvSUwyMHZNRFZxYUdjU0JtVnpMVFF4T1JvQ1EwOG9BQVAB/sections/CAQiTkNCQVNOQW9JTDIwdk1EVnFhR2NTQm1WekxUUXhPUm9DUTA4aURnZ0VHZ29LQ0M5dEx6QXhiSE15S2d3S0NoSUlRMjlzYjIxaWFXRW9BQSowCAAqLAgKIiZDQkFTRmdvSUwyMHZNRFZxYUdjU0JtVnpMVFF4T1JvQ1EwOG9BQVABUAE?hl=es-419&gl=CO&ceid=CO%3Aes-419',
        # 'https://news.google.com/topics/CAAqLAgKIiZDQkFTRmdvSUwyMHZNRFZxYUdjU0JtVnpMVFF4T1JvQ1EwOG9BQVAB/sections/CAQiVENCQVNPUW9JTDIwdk1EVnFhR2NTQm1WekxUUXhPUm9DUTA4aURnZ0VHZ29LQ0M5dEx6QTVibTFmS2hFS0R4SU5TVzUwWlhKdVlXTnBiMjVoYkNnQSowCAAqLAgKIiZDQkFTRmdvSUwyMHZNRFZxYUdjU0JtVnpMVFF4T1JvQ1EwOG9BQVABUAE?hl=es-419&gl=CO&ceid=CO%3Aes-419',

    ]

    def parse(self, response:HtmlResponse, **kwargs):
        storys = response.xpath('//main/c-wiz/div/div/main/div[1]/div')
        for story in storys:
            story_url = response.urljoin(story.xpath('./div/div/*[4]/span/div/a/@href').get())
            articles = story.xpath('.//article')
            story_title = ''
            for i_article,article in enumerate(articles):
                article_url = response.urljoin(article.xpath('./a/@href').get())
                article_title = article.xpath('./*[2]/a/text()').get()
                if i_article==0:
                    story_title = article_title
                    
                itemdata = {
                    'type': 'article',
                    'article_url':article_url,
                    'article_title':article_title,
                    'is_root_article':i_article==0,
                    'story_url': story_url,
                    'story_title':story_title,
                }
                
                yield scrapy.Request(article_url, callback=self.parse_jump_url, cb_kwargs={'itemdata':itemdata})

    def parse_jump_url(self, response:HtmlResponse, **kwargs):
        jump_url = response.xpath('//c-wiz/div/div[2]/c-wiz/div[3]/a/@href').get()
        kwargs['itemdata']['url'] =jump_url
        yield scrapy.Request(response.urljoin(jump_url), self.parse_article, cb_kwargs=kwargs)

    def parse_article(self, response:HtmlResponse, **kwargs):
        itemdata = kwargs['itemdata']
        yield itemdata
