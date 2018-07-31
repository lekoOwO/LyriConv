import re
import requests
from bs4 import BeautifulSoup, element
from bs4.element import NavigableString

def search(song_name):
    def get_content_from_span(y):
        return ''.join(map(lambda x:x if type(x)==NavigableString else x.contents[0], y.contents[0].contents))
    
    def get_id_from_span(x):
        return re.match(r'\/(.+).htm(?:.*)', x.contents[0]['href']).group(1)

    def get_index(index):
        return 2*index-1

    def get_url(url):
        return 'https://mojim.com' + url

    
    req = requests.get('https://mojim.com/{}.html?t3'.format(song_name))

    return {
        'result': {
            "songs": [
                {
                    "id": get_id_from_span(j.contents[get_index(4)]),
                    "name": get_content_from_span(j.contents[get_index(4)]),
                    "artist": {
                        "name": get_content_from_span(j.contents[get_index(2)]),
                        "id": get_id_from_span(j.contents[get_index(2)]),
                        "url": get_url(j.contents[get_index(2)].contents[0]['href'])
                    },
                    "album": {
                        "name": get_content_from_span(j.contents[get_index(3)]),
                        "id": get_id_from_span(j.contents[get_index(3)]),
                        "url": get_url(j.contents[get_index(3)].contents[0]['href'])
                    },
                    "url": get_url(j.contents[get_index(4)].contents[0]['href'])
                } 
                for j in BeautifulSoup(req.text, 'lxml').findAll('dd', {
                    'class': re.compile("mxsh_dd(?:1|2)")
                    })]
                },
        "code": 200
        }

def get_lyric(url):
    if not re.match(r'(?:http|https)\:\/\/mojim\.com\/.+\.(?:htm|html)', url):
        return {"code": 403}
    
    req = requests.get(url)
    lyrics = BeautifulSoup(req.text, 'html.parser').find(id='fsZx3').get_text('\n','<br/>')
    try:
        r = re.match(r"((?:.|\n)+?)\n*(\[(?:.|\n)+\].*\n)(?:(?:.|\n)*)?", lyrics, flags=re.MULTILINE).groups()
    except AttributeError:
        r = [lyrics, None]
    
    return {
        "lrc": r[0],
        "tlyric": r[1],
        "code": 200
    }