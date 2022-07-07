import json 
from datetime import datetime, timedelta
from msilib.schema import File

from khl.card import CardMessage, Card, Module, Element, Types, Struct
from khl import Message, Bot, EventTypes, Event


from src.library.music163 import Music163
# load config from config/config.json, replace `path` to your own config file
# config template: `./config/config.json.example`
with open('../config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# init Bot
bot = Bot(token=config['token'])


@bot.command()
async def minfo(msg: Message, text):
    params = {
        "keywords": text
    }
    result = Music163().GET_DICT('search', params)
    top = result['result']['songs'][0]
    name = top['name']
    artists = top['artists']
    album = top['album']
    artists_name = ''
    album_name = album['name']
    for x in artists:
        artists_name = artists_name + x['name'] + ' '
    await msg.reply(
        CardMessage(
            Card(
                Module.Header(name),
                Module.Context(artists_name),
                Module.Divider(),
                Module.Section(album_name)
            )
        )
    )

@bot.command()
async def mcard(msg: Message,*text):
    text_str = ''
    for x in text:
        text_str = text_str + x + ' '
    params = {
        "keywords": text_str
    }
    search_result = Music163().GET_DICT('search', params)
    top = search_result['result']['songs'][0]
    top_id = top['id']
    result = Music163().GET_DICT('song/url', {'id':top_id})
    result_detail = Music163().GET_DICT('song/detail', {'ids':top_id})
    url = result['data'][0]['url']
    pic_url = result_detail['songs'][0]['al']['picUrl']
    artists = top['artists']
    artists_name = ''
    for x in artists:
        artists_name = artists_name + x['name'] + ' '
    
    await msg.reply(
        CardMessage(
            Card(
                Module.Section(
                    text = top['name'] + '        by :  ' + artists_name,
                    mode = Types.SectionMode.LEFT,
                    accessory = Element.Image(src = pic_url)
                    ),
                Module.Divider(),
                Module.File(type=Types.File.AUDIO,src=url)
            )
        )
    )





# button example, build a card in a single statement
# btw, short code without readability is not recommended
@bot.command()
async def button(msg: Message):
    await msg.reply(
        CardMessage(
            Card(
                Module.Header('An example for button'),
                Module.Context('Take a pill, take the choice'),
                Module.ActionGroup(
                    # RETURN_VAL type(default): send an event when clicked, see print_btn_value() defined at L58
                    Element.Button('Truth', 'RED', theme=Types.Theme.DANGER),
                    Element.Button('Wonderland', 'BLUE', Types.Click.RETURN_VAL)),
                Module.Divider(),
                Module.Section(
                    'another kind of button, user will goto the link when clicks the button:',
                    # LINK type: user will open the link in browser when clicked
                    Element.Button('link button', 'https://github.com/Knoooooooow/khl-chat_bot', Types.Click.LINK)))))



@bot.on_event(EventTypes.MESSAGE_BTN_CLICK)
async def print_btn_value(_: Bot, e: Event):
    print(
        f'''{e.body['user_info']['nickname']} took the {e.body['value']} pill''')


# everything done, go ahead now!
bot.run()
