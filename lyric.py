import json
import requests
import re
from functools import reduce

def chs_to_cht(chs):
    return json.loads(requests.post('https://api.zhconvert.org/convert', data = {'text': chs, 'converter': 'Taiwan'}).text)['data']['text']

offset = (0.0001,4)
parse_lyric = lambda x:re.findall('(?:\[(.+?)\])(.*|\n)', x)
tag_to_sec = lambda x:sum([float(list(reversed(x.split(":")))[i]) * (60 ** i) for i in range(len(list(reversed(x.split(":")))))]) if x[0].isdigit() else x
plyric_to_ptlyric = lambda x:[(x[i+1 if i!=len(x)-1 else i][0] + (-offset[0] if i!=len(x)-1 else offset[0]) if type(x[i][0]) == float else x[i][0], x[i][1]) for i in range(len(x))]
plyric_to_lyric = lambda x:reduce(lambda b,c:b+'\n'+c, map(lambda a:(('[{:.0f}:{:.%sf}]{}' % offset[1]) if type(a[0]) == float else '[{}]{}').format(*(divmod(a[0], 60) if type(a[0]) == float else [a[0]]), a[1]), x))

def migrate(org, translated):
    migrated = org + '\n' + plyric_to_lyric(plyric_to_ptlyric([(tag_to_sec(i[0]), i[1]) for i in parse_lyric(translated)]))
    pmigrated = [[tag_to_sec(i[0]), i[1]] for i in parse_lyric(migrated)]
    for i in range(len(pmigrated)-1):
        if pmigrated[i][1] == '' and type(pmigrated[i+1][0]) == float and pmigrated[i+1][1]!='' and i>0 and type(pmigrated[i-1][0]) == float:
            pmigrated[i+1][0] =  pmigrated[i][0] - offset[0]
    return '\n'.join(['[{}]{}'.format(x[0], x[1]) for x in sorted(parse_lyric(plyric_to_lyric(pmigrated)), key=lambda x:0 if not x[0][0].isdigit() else tag_to_sec(x[0]))])