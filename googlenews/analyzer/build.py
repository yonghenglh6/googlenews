from googlenews.utils.registry import Registry
from scrapy.http.response.html import HtmlResponse


ANALYZER_REGISTRY = Registry("ANALYZER")


def analyze(response:HtmlResponse, **kwargs):
    url = response.url
    url_base_website = '/'.join(url.split('/')[2:3]).replace('.','_')
    return ANALYZER_REGISTRY.get('analyze_'+url_base_website)(response, **kwargs)
