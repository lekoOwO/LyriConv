import pylrc
import json
import requests
import re
from functools import reduce

def chs_to_cht(chs):
    return json.loads(requests.post('https://api.zhconvert.org/convert', data = {'text': chs, 'converter': 'Taiwan'}).text)['data']['text']

parse_lyric = lambda x:re.findall('(?:\[(.+?)\])(.+)', pylrc.parse(x).toLRC())
tag_to_sec = lambda x:round(sum([float(list(reversed(x.split(":")))[i]) * (60 ** i) for i in range(len(list(reversed(x.split(":")))))]), 3)
plyric_to_ptlyric = lambda x:[(round(x[i+1 if i!=len(x)-1 else i][0] + (-0.01 if i!=len(x)-1 else 0.01), 3), x[i][1]) for i in range(len(x))]
plyric_to_lyric = lambda x:reduce(lambda b,c:b+'\n'+c, map(lambda a:'[{:.0f}:{:.2f}]{}'.format(*divmod(a[0], 60), a[1]), x))

def migrate(org, translated):
    return pylrc.parse(org + plyric_to_lyric(plyric_to_ptlyric([(tag_to_sec(i[0]), i[1]) for i in parse_lyric(translated)]))).toLRC()

    

