import requests
import json

with open('../config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

api = config['juhe_api']

from datetime import datetime

cache = {
    "day":'-1/-1',
    "payload":[]
}
class JUHE_API():

    history_today = "todayOnhistory/queryEvent.php"
    url_prefix = api['proxy']
    key = api['key']
    def GET_DICT(self,url,params = {},headers = {}):

        # 10/31
        now_m_d = str(datetime.now().month) + '/' + str(datetime.now().day)
        
        if cache['day']==now_m_d:
            return cache['payload']
        
        url = self.url_prefix + url
        params['key'] = self.key

        res = requests.get(url=url,params = params,headers = headers,timeout=20000)
        to_UTF8 = str(res.content, "utf-8")
        to_json = json.loads(to_UTF8)

        cache['payload'] = to_json
        cache['day'] = now_m_d

        return to_json


