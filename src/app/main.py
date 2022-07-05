import json

from khl import Message, Bot

# load config from config/config.json, replace `path` to your own config file
# config template: `./config/config.json.example`
with open('../config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# init Bot
bot = Bot(token=config['token'])


# register command
# invoke this via saying `!roll 1 100` in channel
# or `/roll 1 100 5` to dice 5 times once
@bot.command()
async def m(msg: Message, name):
    await msg.reply(f'您想点的歌曲为: {name}')


# everything done, go ahead now!
bot.run()
