import json ,requests
from datetime import datetime, timedelta

from khl.card import CardMessage, Card, Module, Element, Types, Struct
from khl import Message, Bot, EventTypes, Event


# from library.music163 import Music163
# load config from config/config.json, replace `path` to your own config file
# config template: `./config/config.json.example`
with open('../config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# init Bot
bot = Bot(token=config['token'])


# register command
# saying `!m 好久不见` in channel
# or `/m 好久不见`
@bot.command()
async def m(msg: Message, name):
    params = {
        "keywords": name
    }
    Music163().GET_DICT('search', params)
    await msg.reply('您想点的歌曲为: {name}')


@bot.command()
async def minfo(msg: Message, text):
    params = {
        "keywords": text
    }
    result = Music163().GET_DICT('search', params)
    top = result.songs[0]
    name = top.name
    artists = top.artists
    album = top.album
    artists_name = ''
    album_name = album.name
    for x in artists:
        artists_name = artists_name + x.name + ' '
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
async def countdown(msg: Message):
    cm = CardMessage()

    # color=(90,59,215) is another available form
    c1 = Card(Module.Header('Countdown example'), color='#5A3BD7')
    c1.append(Module.Divider())
    c1.append(Module.Countdown(datetime.now() +
              timedelta(hours=1), mode=Types.CountdownMode.SECOND))
    cm.append(c1)

    # priority: color > theme, default: Type.Theme.PRIMARY
    c2 = Card(theme=Types.Theme.DANGER)
    c2.append(Module.Section('the DAY style countdown'))
    c2.append(Module.Countdown(datetime.now() +
              timedelta(hours=1), mode=Types.CountdownMode.DAY))
    cm.append(c2)  # A CardMessage can contain up to 5 Cards

    await msg.reply(cm)


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
                    Element.Button('link button', 'https://github.com/TWT233/khl.py', Types.Click.LINK)))))


# struct example
@bot.command()
async def struct(msg: Message):
    await msg.reply(CardMessage(Card(Module.Section(Struct.Paragraph(3, 'a', 'b', 'c')))))


@bot.on_event(EventTypes.MESSAGE_BTN_CLICK)
async def print_btn_value(_: Bot, e: Event):
    print(
        f'''{e.body['user_info']['nickname']} took the {e.body['value']} pill''')

api = config['music_163']['proxy']


class Music163():

    def GET_DICT(self,url,params = {}):
        url = api + url
        res = requests.get(url=url,params = params)
        to_UTF8 = str(res.content, "utf-8")
        to_json = json.loads(to_UTF8)
        return to_json



# everything done, go ahead now!
bot.run()
