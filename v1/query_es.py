import json

import components.fofa_sdk.client as client
from config import secure

# fofa_client = client.Client(secure.EMAIL, secure.KEY)
# query = '''port=9200&&region=TW'''
# query_es = '''protocol==elastic && region=TW'''
# fields = "ip, banner"
# data = fofa_client.get_data(query_str=query_es, fields=fields, page=1, size=200)
#
# with open('test.json', 'w') as f:
#     f.write(json.dumps(data['results']))
# print(len(data))
from util.util import Check

if __name__ == '__main__':
    with open('test.json', 'r', encoding='utf8') as f:
        data = json.load(f)

    for ips in data:
        k = ips[0]
        res = Check.getHttpStatusCode('http://{0}:9200'.format(k))
        if res is 200:
            print('{0}:GREEN'.format(k))
        else:
            print('{0}:NO RES'.format(k))
