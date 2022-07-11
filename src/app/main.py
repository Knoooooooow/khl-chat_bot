import json
import random
from datetime import datetime, timedelta
from msilib.schema import File

from khl.card import CardMessage, Card, Module, Element, Types, Struct
from khl import Message, Bot, EventTypes, Event, MessageTypes


from src.library.music163 import Music163
# load config from config/config.json, replace `path` to your own config file
# config template: `./config/config.json.example`
with open('../config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# init Bot
bot = Bot(token=config['token'])


@bot.command()
async def 卖个萌(msg: Message):
    meng = config['data']['meng']
    meng_int = random.randint(0, len(meng) - 1)
    await msg.reply(meng[meng_int]['text'])


@bot.command()
async def msearch(msg: Message, *text):
    text_str = ''
    for x in text:
        text_str = text_str + x + ' '
    params = {
        "keywords": text_str
    }
    search_result = Music163().GET_DICT('search', params)
    list = search_result['result']['songs']

    showList = []
    for x in list:
        artists = x['artists']
        artists_name = ''
        for y in artists:
            artists_name = artists_name + y['name'] + ' / '
        artists_name = artists_name.strip(' ')
        artists_name = artists_name.strip('/')

        btn_value = {
            "type":"music_163_%s" % 'mcard',
            "value":{}
        }
        btn_value['type'] = "music_163_%s" % 'mcard'
        btn_value['value']['id'] = x['id']
        btn_value['value']['name'] = x['name']
        btn_value['value']['artists_name'] = artists_name
        showList.append(
            {"id": x['id'], "name": x['name'], "artists_name": artists_name, "btn_value": str(btn_value)})

    await msg.reply(CardMessage(Card(

        Module.Section(
            text=Element.Text("**"+showList[0]['name']+"**" + '    ' + r'`' +
                                showList[0]['artists_name'] + r'`', type=Types.Text.KMD),
            mode=Types.SectionMode.LEFT,
            accessory=Element.Button('我要听这个！', showList[0]['btn_value'], Types.Click.RETURN_VAL)
        ),
        Module.Divider(),
        Module.Section(
            text=Element.Text("**"+showList[1]['name']+"**" + '    ' + r'`' +
                                showList[1]['artists_name'] + r'`', type=Types.Text.KMD),
            mode=Types.SectionMode.LEFT,
            accessory=Element.Button('是这首', showList[1]['btn_value'], Types.Click.RETURN_VAL)
        ),
        Module.Divider(),
        Module.Section(
            text=Element.Text("**"+showList[2]['name']+"**" + '    ' + r'`' +
                                showList[2]['artists_name'] + r'`', type=Types.Text.KMD),
            mode=Types.SectionMode.LEFT,
            accessory=Element.Button('是这首', showList[2]['btn_value'], Types.Click.RETURN_VAL)
        ),
        Module.Divider(),
        Module.Section(
            text=Element.Text("**"+showList[3]['name']+"**" + '    ' + r'`' +
                                showList[3]['artists_name'] + r'`', type=Types.Text.KMD),
            mode=Types.SectionMode.LEFT,
            accessory=Element.Button('是这首', showList[3]['btn_value'], Types.Click.RETURN_VAL)
        ),
        Module.Divider(),
        Module.Section(
            text=Element.Text("**"+showList[4]['name']+"**" + '    ' + r'`' +
                                showList[4]['artists_name'] + r'`', type=Types.Text.KMD),
            mode=Types.SectionMode.LEFT,
            accessory=Element.Button('是这首', showList[4]['btn_value'], Types.Click.RETURN_VAL)
        ),

    )
    ))


@ bot.command()
async def mcard(msg: Message, *text):
    text_str = ''
    for x in text:
        text_str = text_str + x + ' '
    params = {
        "keywords": text_str
    }
    search_result = Music163().GET_DICT('search', params)
    top = search_result['result']['songs'][0]
    top_id = top['id']
    result = Music163().GET_DICT('song/url', {'id': top_id, 'br': 320000})
    result_detail = Music163().GET_DICT('song/detail', {'ids': top_id})
    url = result['data'][0]['url']
    pic_url = result_detail['songs'][0]['al']['picUrl']
    artists = top['artists']
    artists_name = ''
    for x in artists:
        artists_name = artists_name + x['name'] + ' / '
    artists_name = artists_name.strip(' ')
    artists_name = artists_name.strip('/')
    await msg.reply(
        CardMessage(
            Card(
                Module.Section(
                    text=Struct.Paragraph(1, Element.Text(
                        "**"+top['name']+"**" + '    ' + r'`' + artists_name + r'`', type=Types.Text.KMD)),
                    mode=Types.SectionMode.LEFT,
                    accessory=Element.Image(src=pic_url)
                ),
                Module.Divider(),
                Module.File(type=Types.File.AUDIO, src=url)
            )
        )
    )


@ bot.on_event(EventTypes.MESSAGE_BTN_CLICK)
async def print_btn_value(b: Bot, e: Event):
    value_str = e.body['value']
    value = eval(value_str)
    channel = await b.fetch_public_channel(e.body['target_id'])
    if value['type'] == "music_163_%s" % 'mcard':
        payload = value['value']
        print(payload)
        top_id = payload['id']
        name = payload['name']
        artists_name = payload['artists_name']
        result = Music163().GET_DICT('song/url', {'id': top_id, 'br': 320000})
        result_detail = Music163().GET_DICT('song/detail', {'ids': top_id})
        url = result['data'][0]['url']
        pic_url = result_detail['songs'][0]['al']['picUrl']
        await b.send(channel,content= CardMessage(
            Card(
                Module.Section(
                    text=Struct.Paragraph(1, Element.Text(
                        "**"+name+"**" + '    ' + r'`' + artists_name + r'`', type=Types.Text.KMD)),
                    mode=Types.SectionMode.LEFT,
                    accessory=Element.Image(src=pic_url)
                ),
                Module.Divider(),
                Module.File(type=Types.File.AUDIO, src=url)
            )
        ),type=MessageTypes.CARD)
    


# everything done, go ahead now!
bot.run()
