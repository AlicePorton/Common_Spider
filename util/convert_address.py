import json

import requests


def get_ll(address):
    address = "台湾省"+address
    addressAPI = "http://api.map.baidu.com/geocoder/v2/?address="+ address+"&output=json&ak=B9DG2Fxl5KjlUymnS1aapUWL"
    content = requests.get(url=addressAPI).content
    result = json.loads(content)
    pass

get_ll("新北市土城区中山路66号")
