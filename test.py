import collections

Premium = collections.namedtuple('premium', 'kind factor')

with open('premia.txt', 'r', encoding='utf-8') as reader:
    dict = collections.OrderedDict()
    for i in reader:
        i = i.rstrip().replace('(', '').replace(')', '')
        pairs = i.split(':')
        p = pairs[1].split(',')
        dict.update({tuple(pairs[0].split(',')): Premium(p[0], int(p[1]))})


    for i in dict:
        print(i, dict[i])