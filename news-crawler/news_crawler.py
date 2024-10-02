### 20249184 방준영 DFMBA 6기

# https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=101
import pdb # python debugger 
import datetime as dt 
import requests

from urllib.parse import urlparse

from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup

NAVER_URL = 'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=101'
NAVER_HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

def fetch_last_page(datestr):

    url = f"{NAVER_URL}&date={datestr}&page=1000"

    resp = requests.get(url)
    # print(resp.status_code)
         
########################################################################################################################
    soup = BeautifulSoup(resp.text, 'html.parser') #html.parser를 사용하렴. 
    paging = soup.find('div',{'class': 'paging'}) # div 컴포넌트를 찾돼, class가 paging인 애를 찾아라 {중괄호}
    strong = paging.find('strong') #paging 안에서 strong 찾아줘. 
    last_page = int(strong.text)
########################################################################################################################      


    # pdb.set_trace() # break point
    # pass

    return last_page

def fetch_news_list(datestr, page):
    print(f"Fetching page {page}... ")

    url = f"{NAVER_URL}&date={datestr}&page={page}"
    
    # pdb.set_trace()
    
    resp = requests.get(url) # Request -> Response
    soup = BeautifulSoup(resp.text, 'html.parser')

    list_body = soup.find('div', {'class' : 'list_body'})
    
    buffer = []

    for item in list_body.find_all('li'):
        link = item.find_all('a')[-1]
        title = link.text.strip()
        url = link['href']
        
        parsed_url = urlparse(url) # 앞에꺼 머리, 꽁지 제외하고, API PATH만 찾아준다.
        tokens = parsed_url.path.split('/')

        doc_id = 'nn-' + '-'.join(tokens[-2:])
       
        # print(title)
        # print(url)

        entry = (doc_id, title, url) # item을 튜플 형식으로 저장. 
        # pdb.set_trace()
        buffer.append(entry)


    return buffer

def parse_media_info(soup):

    media_info = soup.find('div', {'class' : 'media_end_head_info_datestamp'})
    
    if media_info:
        datestr_list = media_info.find_all('span', 'media_end_head_info_datestamp_time') ##수정 일자도 있을 때도 있음.

        link = media_info.find('a' , {'class' : 'media_end_head_origin_link'})
        source_url = link['href'] if link else '' # source_url = link 비어있으면, ''로 치환. 


        return datestr_list, source_url
        

    else:
        raise RuntimeError

    pass

def parse_datestr(span):
    # data-date-time="2024-09-01 23:55:07" -> 꺼내오자.

    if span.has_attr('data-date-time'):
        datestr = span['data-date-time']
    elif span.has_attr('data-modify-date-time'):  
        datestr = span['data-modify-date-time']
    else:
        return None
    
    date = dt.datetime.fromisoformat(datestr) #YYYY-mm-dd 시간:분:초 iso로 전환한다. 

    return date


def fetch_news_body(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    # print(resp.status_code)

    title = soup.title.text.strip() # 빈공간 없애줘. 

    node = soup.find('meta', {'property' : 'og:article:author'}) # <meta property="og:article:author" content="이데일리 | 네이버">

    if node: #if 노드가 있으면.. 
        content = node['content'] 

        if '네이버 스포츠' in content:
            return None # 처리하지말고 none. 오류 방지용
        
        if 'TV연예' in content:
            return None # Reverse Engineering. 오류 방지용
        
        tokens = content.split('|')
        publisher = tokens[0].strip() #strip: 빈공간 없애줘!  , # 언론사 정보 꺼내오기(Ex, 이데일리) 

    else:
        raise RuntimeError() #문제가 있을 때 바로 죽는게 좋다. 예외처리. 
    
    # 2024-09-01 23:55:07 찾기
    # <span class="media_end_head_info_datestamp_time _ARTICLE_DATE_TIME" data-date-time="2024-09-01 23:55:07" data-date-time-age-in-minutes="44381">2024.09.01. 오후 11:55</span>
    
    datestr_list, source_url = parse_media_info(soup)

    if len(datestr_list) == 1: # 1개: 생성날짜가 하나다. 
        created_at = parse_datestr(datestr_list[0])
        updated_at = created_at
    
    elif len(datestr_list) == 2: # 2개: 생성/수정 날짜가 둘다 있다.
        created_at = parse_datestr(datestr_list[0])
        updated_at = parse_datestr(datestr_list[1])

    else:
        raise RuntimeError()
    

    body = soup.find('div', {'id': 'newsct_article'})

    assert body is not None # body 반드시 잇어야해
    body_text = body.text.strip()

    images = body.find_all('img')
    image_urls = [ x.get('src') or x.get('data-src') for x in images ] #src 혹은 data-src로 들어가있다.. 해결법)
        # 비교하기, x.get('src') VS x['src']
        # (1) x.get('src') -> src없으면 None 반환
        # (2) x['src'] -> src없으면 에러 반환
        # -> 존재할 때는 둘다 동일

    image_urls = list[set(image_urls)]
        #set을 통해 중복 제거 가능하다. 


    # print(title)
    # print(publisher)
    # print(datestr_list)
    # print(source_url)
    # print(created_at) #생성 일자일시
    # print(updated_at) #수정 일자일시
    # print(body_text)
    # print(image_urls)

    entry = {
        'title' : title,
        'section' : 'economy',
        'naver_url': url,
        'source_url' : source_url, 
        'image_urls' : image_urls,
        'publisher' : publisher,
        'created_at' : created_at.isoformat(), # iso 포맷으로........아까는 International standard 문자열 -> iso
        'updated_at' : updated_at.isoformat(),
        'body' : body_text
    } # 하나의 Dic로 묶어주자. 
    
    print(entry)
    return entry

def fetch_news_list_for_date(date):

    datestr = date.strftime('%Y%m%d') # Y 2024, m 03, d 30

    print(f"Fetching news list on {datestr}")

    last_page = fetch_last_page(datestr)

    for page in range(1, last_page + 1):  
        items = fetch_news_list(datestr, page)

        for doc_id, title, url in items: #items에는 신문 기사의 목록(List)가 담겨 있다.  -> 튜플 (entry)

            print(f"[{doc_id}] {title}")

            body = fetch_news_body(url)

            pdb.set_trace()

if __name__ == '__main__':
    base_date = dt.datetime(2024, 9, 1)

    for d in range(1):
        date = base_date + relativedelta(days = d)

        fetch_news_list_for_date(date) #F12로 하면 메소드 안으로 들어감
 