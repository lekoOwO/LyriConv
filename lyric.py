import json
import requests
import re
from functools import reduce

def chs_to_cht(chs):
    return json.loads(requests.post('https://api.zhconvert.org/convert', data = {'text': chs, 'converter': 'Taiwan'}).text)['data']['text']

offset = (0.0001,4)
parse_lyric = lambda x:re.findall('(?:\[(.+?)\])(.*|\n)', x)
tag_to_sec = lambda x:sum([float(list(reversed(x.split(":")))[i]) * (60 ** i) for i in range(len(list(reversed(x.split(":")))))]) if type(x) == str and x[0].isdigit() else x
get_next_index = lambda x,y:y.index(list(filter(lambda k:False if not type(k[0]) == float else -10*offset[0] <= tag_to_sec(k[0])-x[0] <= 10*offset[0], y))[0])+1
plyric_to_ptlyric = lambda x,y:[(i[0] if type(i[0]) != float else y[-1][0]+offset[0] if get_next_index(i,y) >= len(y) else y[get_next_index(i,y)][0] - offset[0], i[1]) for i in x]
plyric_to_lyric = lambda x:reduce(lambda b,c:b+'\n'+c, map(lambda a:(('[{:.0f}:{:.%sf}]{}' % offset[1]) if type(a[0]) == float else '[{}]{}').format(*(divmod(a[0], 60) if type(a[0]) == float else [a[0]]), a[1]), x))

def migrate(org, translated):
    migrated = org + '\n' + plyric_to_lyric(plyric_to_ptlyric([(tag_to_sec(i[0]), i[1]) for i in parse_lyric(translated)], [(tag_to_sec(i[0]), i[1]) for i in parse_lyric(org)]))
    pmigrated = sorted([[tag_to_sec(i[0]), i[1]] for i in parse_lyric(migrated)], key=lambda x:x[0] if type(x[0]) == float else 0)
    return plyric_to_lyric(sorted(parse_lyric(plyric_to_lyric(pmigrated)), key=lambda x:0 if not x[0][0].isdigit() else tag_to_sec(x[0])))