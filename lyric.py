import pylrc
import json
import requests
import re
from functools import reduce

def chs_to_cht(chs):
    return json.loads(requests.post('https://api.zhconvert.org/convert', data = {'text': chs, 'converter': 'Taiwan'}).text)['data']['text']

parse_lyric = lambda x:re.findall('(?:\[(.+?)\])(.*|\n)', pylrc.parse(x).toLRC())
tag_to_sec = lambda x:round(sum([float(list(reversed(x.split(":")))[i]) * (60 ** i) for i in range(len(list(reversed(x.split(":")))))]), 3) if x[0].isdigit() else x
plyric_to_ptlyric = lambda x:[(round(x[i+1 if i!=len(x)-1 else i][0] + (-0.01 if i!=len(x)-1 else 0.01), 3) if type(x[i][0]) == float else x[i][0], x[i][1]) for i in range(len(x))]
plyric_to_lyric = lambda x:reduce(lambda b,c:b+'\n'+c, map(lambda a:('[{:.0f}:{:.2f}]{}' if type(a[0]) == float else '[{}]{}').format(*divmod(a[0], 60) if type(a[0]) == float else a[0], a[1]), x))

def migrate(org, translated):
    migrated = pylrc.parse(org + '\n' + plyric_to_lyric(plyric_to_ptlyric([(tag_to_sec(i[0]), i[1]) for i in parse_lyric(translated)]))).toLRC()
    pmigrated = [[tag_to_sec(i[0]), i[1]] for i in re.findall('(?:\[(.+?)\])(.*|\n)', migrated)]
    for i in range(len(pmigrated)-1):
        if pmigrated[i][1] == '' and type(pmigrated[i+1][0]) == float and pmigrated[i+1][1]!='' :
            pmigrated[i+1][0] =  pmigrated[i][0] - 0.01
    return pylrc.parse(plyric_to_lyric(pmigrated)).toLRC()

    

