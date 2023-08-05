import asyncio
import constants
import discord
import dbl
import aiohttp
import logging
from discord.ext import commands
from utilities import utilities

client = discord.Client()

class DiscordBotsOrgAPI:
    """Handles interactions with the discordbots.org API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = ""  #  set this to your DBL token
        self.dblpy = dbl.Client(self.bot, self.token)
        self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""
        print("I got here")
        while True:
            print('attempting to post server count')
            try:
                await self.dblpy.post_server_count()
                print('posted server count ({})'.format(len(client.servers)))
            except Exception as e:
                print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
            await asyncio.sleep(1800)


def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(DiscordBotsOrgAPI(bot))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('Hello world!')
    print('------')
    await client.change_presence(game=discord.Game(name='$help $invite'))
    new_bot = DiscordBotsOrgAPI(client)
    await new_bot.update_stats()

@client.event
async def on_message(message):
    await utilities.run_commands(message, client)

client.run(constants.bot_key)
