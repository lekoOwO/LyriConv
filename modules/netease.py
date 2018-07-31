import requests
from lyric import chs_to_cht

def search(s, type_=1, offset=0):
    # 歌曲 : 1
    # 專輯 : 10
    # 歌手 : 100
    # 歌單 : 1000
    # 用戶 : 1002
    # MV : 1004 
    # 歌詞 : 1006
    # 電台 : 1009

    return requests.post('https://music.163.com/api/search/get', 
        headers = {
        "Cookie": 'appver=2.0.2',
        "Referer": 'https://music.163.com'
        }, params = {
            "s": s,
            "type": type_,
            "offset": offset,
            "total": True,
            "limit": 20
        }).json()

def get_lyric(id_):
    i = requests.post('https://music.163.com/api/song/lyric', 
        headers = {
        "Cookie": 'appver=2.0.2',
        "Referer": 'https://music.163.com'
        }, params = {
            "os": 'pc',
            "id": id_,
            "lv": -1,
            "tv": -1
        }).json()

    return {
        "lrc": i.get('lrc').get('lyric'),
        "tlyric": chs_to_cht(i.get('tlyric').get('lyric')),
        "code": i.get("code")
        }