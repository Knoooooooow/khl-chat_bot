import requests
import json

with open('../config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

api = config['music_163']['proxy']


class Music163():

    def GET_DICT(self,url,params = {}):
        url = api + url
        res = requests.get(url=url,params = params)
        to_UTF8 = str(res.content, "utf-8")
        to_json = json.loads(to_UTF8)
        return to_json
# params = {
#     "keywords":"好久不见"
# }
# print(Music().GET_DICT('search',params))