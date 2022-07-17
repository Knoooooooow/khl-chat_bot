import requests
import json

with open('../config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

api = config['roll_tools_api']



class Roll_Tools_API():
    history_today = "history/today"
    url = api['proxy']
    app_id = api['app_id']
    app_secret = api['app_secret']
    def GET_DICT(self,url,params = {},headers = {}):
        url = api + url
        params['app_id'] = self.app_id
        params['app_secret'] = self.app_secret

        res = requests.get(url=url,params = params,headers = headers,timeout=20000)
        to_UTF8 = str(res.content, "utf-8")
        to_json = json.loads(to_UTF8)
        return to_json


