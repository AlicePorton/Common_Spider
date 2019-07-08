from elasticsearch import  Elasticsearch

es = Elasticsearch(['http://192.168.1.23:9200'])

# 获取一个index有多少条数据
es.indices.get_settings()