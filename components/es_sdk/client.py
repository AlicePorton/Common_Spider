import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class Client:
    def __init__(self, host='127.0.0.1', port='9200'):
        self.es = Elasticsearch(host=host, port=port)

    def insert_doc(self, index, doc_type, doc, id):
        result = self.es.index(index=index, doc_type=doc_type, body=doc, id=id)
        if result in result:
            return True
        else:
            return False

    def insert_jsonl(self, path, index, type):
        def gdata():
            for line in open(path, 'r'):
                yield {
                    "_index": index,
                    "_type": type,
                    "doc": json.loads(line)
                }
        bulk(self.es, gdata())


if __name__ == '__main__':
    """
    todo: 需要添加回显信息
    """
    client = Client(host='192.168.1.23')
    client.insert_jsonl(path='test_last.jsonx', index='tw-company', type='business')



