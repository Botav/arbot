import discord
from discord.ext import commands
import secrets
from globals import Globals as g

import traceback
from datetime import datetime
from random import seed

description = '''An example arbot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

# this specifies what extensions to load when the arbot starts up
startup_extensions = ["search", "games", "pokedex"]

arbot = commands.Bot(command_prefix='>', description=description)

@arbot.event
async def on_ready():
    seed(a=None)
    print('Logged in as')
    print(arbot.user.name)
    print('Servers: ' + ', '.join([str(s) for s in arbot.servers]))
    print('------')

@arbot.event
async def on_command(s,e):
    print("{0.name} used >{1} in {2.name} (Channel #{3})".format(e.message.author,s,e.message.server,e.message.channel))

@arbot.event
async def on_command_error(error,ctx):
    # em = discord.Embed(title="An Error occured",description="Sorry but I couldn't process that command properely",color=discord.Color.red())
    # await arbot.send_message(ctx.message.channel,embed=em)
    tb = "\n".join(traceback.format_tb(error.original.__traceback__))
    print("{}: {}\n{}".format(error.original.__class__.__name__,str(error),str(tb)))

@arbot.command()
async def load(extension_name : str):
    """Loads an extension."""
    try:
        arbot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await arbot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await arbot.say("{} loaded.".format(extension_name))

@arbot.command()
async def unload(extension_name : str):
    """Unloads an extension."""
    arbot.unload_extension(extension_name)
    await arbot.say("{} unloaded.".format(extension_name))

@arbot.command()
async def ti():
    '''
    Display the bot's time (PST)
    Usage: !ti
    '''
    now = datetime.now()
    print(now)
    return await arbot.say("Server time is %s:%s:%s PST  %s/%s/%s"
                           % (now.hour, now.minute, now.second, now.month,
                              now.day, now.year), delete_after=10)

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            arbot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    token = secrets.BOT_TOKEN if g.IS_BOT else secrets.USER_TOKEN
    arbot.run(token, bot=g.IS_BOT)
