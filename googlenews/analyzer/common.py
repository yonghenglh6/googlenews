
from .build import ANALYZER_REGISTRY
from scrapy.http.response.html import HtmlResponse
from scrapy.shell import inspect_response
import json

def parse_html_to_text_by_xpath(response, node_xpath, join_char=''):
    alltexts = response.xpath(node_xpath+'//text()'+' | '+ node_xpath+'//br').getall()
    mixed_text= join_char.join(alltexts).replace('<br>',' \n').replace('<br />',' \n').replace('<br/>',' \n').strip()
    return mixed_text.strip()

@ANALYZER_REGISTRY.register()
def analyze_www_eltiempo_com(response:HtmlResponse, **kwargs):
    titulo = parse_html_to_text_by_xpath(response, '/html/body/div[2]/article/div[2]/section/div[2]/div[3]')
    article_epigraph = parse_html_to_text_by_xpath(response, '/html/body/div[2]/article/div[2]/div[2]/div[2]/div[3]')
    contenido_first =  parse_html_to_text_by_xpath(response, '/html/body/div[2]/article/div[2]/div[3]/section/div[1]/div[2]/div[3]/div/p[1]')
    contenidos_left = parse_html_to_text_by_xpath(response, '/html/body/div[2]/article/div[2]/div[3]/section/div[1]/div[2]/div[3]/div/p[position()>1]')
    head_pic = response.xpath('/html/body/div[2]/article/div[2]/section/div[1]/div/div//figure/picture//img/@data-original').get()
    pics = response.xpath('/html/body/div[2]/article/div[2]/div[3]/section/div[1]/div[2]/div[3]/div/div[5]/div[1]/figure')
    # 总是访问被拒绝，感觉没办法爬.....
    return None

@ANALYZER_REGISTRY.register()
def analyze_www_elespectador_com(response:HtmlResponse, **kwargs):
    """
        https://www.elespectador.com/bogota/pruebas-gratis-de-covid-19-los-puntos-habilitados-para-este-20-de-enero/
    """
    title = parse_html_to_text_by_xpath(response, '/html/body/div[1]/div/div[2]/div[2]/section[1]/div[2]/div[2]/div[1]/div/h1')
    alternative_title =  parse_html_to_text_by_xpath(response, '/html/body/div[1]/div/div[2]/div[2]/section[1]/div[2]/div[2]/div[1]/div/div[2]/div')
    content_list = response.xpath('/html/body/div[1]/div/div[2]/div[2]/section[1]/div[2]/div[2]/div[2]/section[1]/article/div[1]/section/p')
    
    sent_list  = [parse_html_to_text_by_xpath(p, '.') for p in content_list]
    sent_list = [sent for sent in sent_list if sent!='']
    abstract,in_abstract= '',True
    # 尝试提取摘要
    for sent in sent_list:
        if len(sent)<40:
            in_abstract = False
        if in_abstract:
            abstract+= sent+'\n'
    content = '\n'.join(sent_list)
    video_url = []
    image_urls = []
    imagedata = response.xpath('/html/body/div[1]/div/div[2]/div[2]/section[1]/div[2]/div[2]/div[2]/section[1]/article/div[1]/section/div[1]/div[1]/picture/img/@src').getall()
    if imagedata:
        image_urls.extend(imagedata)
    parse_result = {
        'title':title,
        'alternative_title':alternative_title,
        'abstract':abstract,
        'content':content,
        'video_url':video_url,
        'image_urls':image_urls,
    }
    return parse_result



@ANALYZER_REGISTRY.register()
def analyze_caracol_com_co(response:HtmlResponse, **kwargs):
    """
        https://caracol.com.co/emisora/2022/01/06/bucaramanga/1641496929_374536.html
        https://caracol.com.co/emisora/2022/01/07/bucaramanga/1641517619_342232.html
    """

    title = parse_html_to_text_by_xpath(response, '/html/body/main/div/article/div/header/h1')
    alternative_title =  parse_html_to_text_by_xpath(response, '/html/body/main/div/article/div/header/h2')
    content_list = response.xpath('/html/body/main/div/article/div/div[2]/div[3]/div[2]/div[1]/p')
    
    sent_list  = [parse_html_to_text_by_xpath(p, '.') for p in content_list]
    sent_list = [sent for sent in sent_list if sent!='']
    abstract,in_abstract= '',True
    # 尝试提取摘要
    for sent in sent_list:
        if len(sent)<40:
            in_abstract = False
        if in_abstract:
            abstract+= sent+'\n'
    content = '\n'.join(sent_list)

    video_url = []
    videodata = response.xpath('/html/body/main/div/article/div/div[1]/script[2]//text()').get()
    if videodata:
        videodata = json.loads(videodata.strip())
        video_url.append(videodata['contentURL'])
    image_urls = []
    imagedata = response.xpath('/html/body/main/div/article/div//figure//img/@data-src').getall()
    if imagedata:
        image_urls.extend(['https:'+u for u in imagedata])
    video_foto_data = response.xpath('/html/body/main/div/article/div/div[1]/div/@data-fotonoticia').getall()
    if video_foto_data:
        image_urls.extend(['https://caracol.com.co'+u for u in video_foto_data])
    return {
        'title':title,
        'alternative_title':alternative_title,
        'abstract':abstract,
        'content':content,
        'video_url':video_url,
        'image_urls':image_urls,
    }


@ANALYZER_REGISTRY.register()
def analyze_www_bluradio_com(response:HtmlResponse, **kwargs):
    """
        https://www.bluradio.com/politica/zuluaga-pasa-la-pagina-con-equipo-por-colombia-critica-que-coalicion-haya-operado-desde-los-vetos
    """
    title = parse_html_to_text_by_xpath(response, '/html/body/bs-page/div[@class="ArticlePage-content"]/div[1]/h1')
    alternative_title =  parse_html_to_text_by_xpath(response, '/html/body/bs-page/div[@class="ArticlePage-content"]/div[1]/h2')
    content_list = response.xpath('/html/body/bs-page/div[@class="ArticlePage-content"]/div[2]/main/div/article/div[3]/div[1]/div/div/p')
    
    sent_list  = [parse_html_to_text_by_xpath(p, '.') for p in content_list]
    sent_list = [sent for sent in sent_list if sent!='']
    abstract,in_abstract= '',True
    # 尝试提取摘要
    for sent in sent_list:
        if len(sent)<40:
            in_abstract = False
        if in_abstract:
            abstract+= sent+'\n'
    content = '\n'.join(sent_list)
    video_url = []
    image_urls = []
    imagedata = response.xpath('/html/body/bs-page/div[@class="ArticlePage-content"]/div[2]/main/div/article/div[1]/figure/picture/img/@src').getall()
    if imagedata:
        image_urls.extend(imagedata)
    parse_result = {
        'title':title,
        'alternative_title':alternative_title,
        'abstract':abstract,
        'content':content,
        'video_url':video_url,
        'image_urls':image_urls,
    }
    return parse_result



def image_website(response:HtmlResponse, title_xpath, alternative_title_xpath, content_list_xpath, imagedata_xpath, **kwargs):
    title = parse_html_to_text_by_xpath(response, title_xpath)
    alternative_title =  parse_html_to_text_by_xpath(response, alternative_title_xpath)
    content_list = response.xpath(content_list_xpath)
    
    sent_list  = [parse_html_to_text_by_xpath(p, '.') for p in content_list]
    sent_list = [sent for sent in sent_list if sent!='']
    abstract,in_abstract= '',True
    # 尝试提取摘要
    for sent in sent_list:
        if len(sent)<40:
            in_abstract = False
        if in_abstract:
            abstract+= sent+'\n'
    content = '\n'.join(sent_list)
    video_url = []
    image_urls = []
    imagedata = response.xpath(imagedata_xpath).getall()
    if imagedata:
        image_urls.extend(imagedata)
    parse_result = {
        'title':title,
        'alternative_title':alternative_title,
        'abstract':abstract,
        'content':content,
        'video_url':video_url,
        'image_urls':image_urls,
    }
    return parse_result

@ANALYZER_REGISTRY.register()
def analyze_www_semana_com(response:HtmlResponse, **kwargs):
    """
        https://www.semana.com/nacion/articulo/oscar-ivan-zuluaga-se-mantiene-ira-solo-a-la-primera-vuelta-presidencial/202206/
        失败，这个网站看起来可能爬不动
    """
    title_xpath='/html/body/div[1]/div/main/div[2]/div[1]/div/header/div[2]/h1'
    alternative_title_xpath='/html/body/div[1]/div/main/div[2]/div[1]/div/header/div[2]/h2'
    content_list_xpath='/html/body/div[1]/div/main/div[2]/div[1]/div/article/p'
    imagedata_xpath='/html/body/div[1]/div/main/div[2]/div[1]/div/header/div[4]/picture/img/@src'

    parse_result = image_website(response=response, 
        title_xpath=title_xpath,
        alternative_title_xpath=alternative_title_xpath,
        content_list_xpath=content_list_xpath,
        imagedata_xpath=imagedata_xpath,
        **kwargs
    )
    return parse_result

