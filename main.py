from discord import Intents
from discord.ext.commands import Bot

from dotenv import load_dotenv
from os import getenv, listdir

load_dotenv()

client = Bot('-', intents = Intents.all())

@client.listen('on_ready')
async def ready():
    print(f'{client.user.name} online!')


def load_cogs(path = 'cogs'):
    for file in listdir(path):
        if not file.startswith('_'):
            if file.endswith('.py'):
                file = f'{path}.{file}'.replace('.py', '')
                client.load_extension(file.replace('/', '.'))

            else:
                load_cogs(path + '/' + file)
 

if __name__ == '__main__':
    load_cogs()
    client.run(getenv('BOT_TOKEN'))


