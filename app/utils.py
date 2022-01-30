from fastapi.params import Query
from app.db.base_class import Page
import re
from enum import Enum
from urllib.parse import urljoin, urlparse
from app.schemes.faucet import FaucetPlatform


MAX_QUERY_STRING_LENGTH = 255

def paginate(page_num: int = 1, page_size: int = 100, query: Query = None):
    if page_num <= 0:
        raise AttributeError('page needs to be >= 1')
    if page_size <= 0:
        if page_size != -1:
            raise AttributeError('page_size needs to be >= 1')
        else:
            items = query.all()
    else:
        items = query.limit(page_size).offset((page_num - 1) * page_size).all()
    total = query.order_by(None).count()
    return Page(items, page_num, page_size, total)

def normalise_query_string(query_string):
    if len(query_string) > MAX_QUERY_STRING_LENGTH:
        query_string = query_string[:MAX_QUERY_STRING_LENGTH]
    query_string = query_string.lower()
    query_string = re.sub(' +', ' ', query_string).strip()
    return query_string

def normalise_url_without_query(url):
    url = url.lower()
    return urljoin(url, urlparse(url).path)

def get_platform(query_string):
    for data in FaucetPlatform:
        if re.search(data.value, query_string):
            return data.value
    return ''

def validate_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url)

# !!! begin with 0x end by \b
def get_address(text):
    o = re.search(r'\b0x.{32}\b', text)
    if o:
        return o.group()
    return ''

def get_twitter_username(url):
    # example: https://twitter.com/Username/status/1434169115296423938

    parse_url = urlparse(url)
    username = parse_url.path.split('/')[1]
    return username