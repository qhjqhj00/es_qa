import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('--source', required=True, type=str)
parser.add_argument('--save', required=True, type=str)
args = parser.parse_args()

def get_qa(l):
    res = []
    tmp = ['','']
    q = False
    a = False
    for i in l:
        if q and i.find('答复：') == -1:
            tmp[0] += i
        elif a and i.find('答复时间') == -1:
            tmp[1] += i
            
        if i.find('问题：') != -1:
            q = True
        elif i.find('答复：') != -1:
            q = False
            a = True
        elif i.find('答复时间') != -1:
            a = False
            res.append(tmp)
            tmp = ['','']
    return res

data = open(args.source).read().strip().split('\n')
qas = []
import json
for d in data:
    try:
        qas.extend(get_qa(json.loads(re.sub('\x00','', d))['content'].split()))
    except:
        pass



with open(args.save, 'w') as f:
    for d in qas:
        d[1] = re.sub('.+同志(:|：)','',d[1])
        f.write(f'{d[0]}\t{d[1]}\n')
    f.truncate()

print(f'now we have {len(qas)}')

