import requests
import json

with open('../config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

api = config['music_163']['proxy']


class Music163():

    cookie = config['music_163']['music_cookie']
    uid = config['music_163']['uid']

    def GET_DICT(self,url,params = {},headers = {}):
        url = api + url
        headers['uid'] = self.uid
        
        if self.cookie !='':
            headers['cookie'] = self.cookie

        res = requests.get(url=url,params = params,headers = headers,timeout=20000)
        to_UTF8 = str(res.content, "utf-8")
        to_json = json.loads(to_UTF8)
        return to_json
        