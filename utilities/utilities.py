from utilities import general_commands
#from utilities import voice_client
from utilities import chat_filter
from utilities import currency
from utilities import prefix
from constants import chat_filter_enable_path
import os

async def run_commands(message, client):

    try:
        server_id = message.server.id
    except:
        c_prefix = "$"
    else:
        c_prefix = prefix.get_prefix(server_id)
        if c_prefix == "":
            c_prefix = "$"

    if message.author.id != "385206243779674132":
        player = None
        if message.content.startswith('{}hello'.format(c_prefix)) or message.content.startswith('{}hey'.format(c_prefix)) or message.content.startswith('{}hi'.format(c_prefix)) or message.content.startswith('{}sup'.format(c_prefix)):
            await general_commands.hello(message, client)
        elif message.content.startswith('{}prefix'.format(c_prefix)):
            await prefix.set_prefix(message, client, "{}".format(c_prefix))
        elif message.content.startswith('{}vote'.format(c_prefix)):
            await general_commands.vote(message, client)
        elif message.content.startswith('{}invite'.format(c_prefix)):
            await general_commands.invite(message, client)
        elif message.content.startswith('{}servercount'.format(c_prefix)):
            await general_commands.server_count(message, client)
        elif message.content.startswith('{}serverinfo'.format(c_prefix)):
            await general_commands.server_info(message, client)
        elif message.content.startswith('{}userinfo'.format(c_prefix)):
            await general_commands.user_info(message, client)
        elif message.content.startswith('{}help'.format(c_prefix)) or message.content.startswith('{}support'.format(c_prefix)):
            await general_commands.support(message, client, c_prefix)
        elif message.content.startswith('{}love'.format(c_prefix)):
            await general_commands.love(message, client, c_prefix)
        elif message.content.startswith('{}coinflip'.format(c_prefix)) or message.content.startswith('{}coin'.format(c_prefix)) or message.content.startswith('{}flipcoin'.format(c_prefix)):
            await general_commands.coinflip(message, client)
        #elif message.content.startswith('{}play'):
        #    player = await voice_client.play(message, client, player)
        #    if player != None:
        #        if player.is_playing():
        #            await voice_client.voice_player(message, client, player)
        #elif message.content.startswith('{}skip'):
        #    await voice_client.skip(message, client)
        #elif message.content.startswith('{}stop'):
        #    await voice_client.stop(message, client)
        #elif message.content.startswith('{}queue'):
        #    await voice_client.queue(message, client)
        elif message.content.startswith('{}rolldice'.format(c_prefix)):
            await general_commands.roll_dice(message, client, c_prefix)
        elif message.content.startswith('{}8ball'.format(c_prefix)):
            await general_commands.eight_ball(message, client)
        elif message.content.startswith('{}cf enable'.format(c_prefix)):
            await chat_filter.enable_chat_filter(message, client)
        elif message.content.startswith('{}cf disable'.format(c_prefix)):
            await chat_filter.disable_chat_filter(message, client)
        elif message.content.startswith('{}cf bl add word'.format(c_prefix)):
            await chat_filter.add_word_to_blacklist(message, client, c_prefix)
        elif message.content.startswith('{}cf wl add word'.format(c_prefix)):
            await chat_filter.add_word_to_whitelist(message, client, c_prefix)
        elif message.content.startswith('{}cf rl add word'.format(c_prefix)):
            await chat_filter.add_word_to_redlist(message, client, c_prefix)
        elif message.content.startswith('{}cf bl add channel'.format(c_prefix)):
            await chat_filter.add_channel_to_blacklist(message, client, c_prefix)
        elif message.content.startswith('{}cf wl add channel'.format(c_prefix)):
            await chat_filter.add_channel_to_whitelist(message, client, c_prefix)
        elif message.content.startswith('{}cf rl add channel'.format(c_prefix)):
            await chat_filter.add_channel_to_redlist(message, client, c_prefix)
        elif message.content.startswith('{}cf bl remove word'.format(c_prefix)):
            await chat_filter.remove_word_from_blacklist(message, client, c_prefix)
        elif message.content.startswith('{}cf wl remove word'.format(c_prefix)):
            await chat_filter.remove_word_from_whitelist(message, client, c_prefix)
        elif message.content.startswith('{}cf rl remove word'.format(c_prefix)):
            await chat_filter.remove_word_from_redlist(message, client, c_prefix)
        elif message.content.startswith('{}cf bl remove channel'.format(c_prefix)):
            await chat_filter.remove_channel_from_blacklist(message, client, c_prefix)
        elif message.content.startswith('{}cf wl remove channel'.format(c_prefix)):
            await chat_filter.remove_channel_from_whitelist(message, client, c_prefix)
        elif message.content.startswith('{}cf rl remove channel'.format(c_prefix)):
            await chat_filter.remove_channel_from_redlist(message, client, c_prefix)
        elif message.content.startswith('{}cf help'.format(c_prefix)):
            await chat_filter.cf_help(message, client)
        #elif message.content.startswith('{}lc start'):
        #    await currency.start_mining(message, client)
        #elif message.content.startswith('{}lc bal'):
        #    await currency.get_user_balance(message, client)
        #elif message.content.startswith('{}lc daily'):
        #    await currency.get_daily_coins(message, client)
        #elif message.content.startswith('{}lc weekly'):
        #    await currency.get_weekly_coins(message, client)
        #elif message.content.startswith('{}lc gamble'):
        #    await currency.gamble_coins(message, client)
        #elif message.content.startswith('{}lc pay'):
        #    await currency.pay_coins(message, client)
        #elif message.content.startswith('{}lc top'):
        #    await currency.global_leaderboard(message, client)
        else:
            try:
                server_id = message.server.id
                if os.path.exists(chat_filter_enable_path.format(server_id)):
                    await chat_filter.whitelist_checker(message, client)
                    await chat_filter.blacklist_checker(message, client)
                    await chat_filter.redlist_checker(message, client)
            except:
                x = None
            else:
                x = None
