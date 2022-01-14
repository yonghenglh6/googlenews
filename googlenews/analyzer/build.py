from googlenews.utils.registry import Registry
from scrapy.http.response.html import HtmlResponse


ANALYZER_REGISTRY = Registry("ANALYZER")



WEBSITE2NAME = {
    'https://www.eltiempo.com/':'eltiempo',  # 防爬虫太厉害了
    'https://caracol.com.co':'caracol',
    'https://www.bluradio.com/':'bluradio',
}

def analyze(response:HtmlResponse, **kwargs):
    url = response.url
    url_base_website = '/'.join(url.split('/')[:3])
    if url_base_website not in WEBSITE2NAME:
        return None
    return ANALYZER_REGISTRY.get('analyze_'+WEBSITE2NAME[url_base_website])(response, **kwargs)
