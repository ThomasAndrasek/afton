from constants import chat_filter_storage_path
from constants import chat_filter_enable_path
from constants import chat_filter_config_path
import os
import sqlite3
import discord

async def cf_help(message, client):
    if message.channel.is_private != True:
        await client.send_message(message.channel, "I am private messaging you support info for the BlackList.")

    await client.send_message(message.author, "**Chat Filter Help**\n" +
                                               "This is a small guide on how to set up a Chat Filter for your discord server.\n" +
                                               "You must also be an admistrator of the discord server to do this.\n\n" +
                                               "__1. Enable the chat filter on your server.__" +
                                               "```$cf enable```" +
                                               "\n__2. Add words to the whitelist or the blacklist chat filter.__\n" +
                                               "The whitelist only lets certain words through while the blacklist blocks certain words, and the redlist blocks the word no matter how it looks. Redlist EX: 'hell' is blocked, so is 'hello'." +
                                               "```$cf [wl, bl, rl] add word <word>\n" +
                                                  "EX. $cf bl add word heck```" +
                                               "\n__3. Add channels for the bot to check in.__" +
                                               "```$cf [wl, bl, rl] add channel <channel>\n" +
                                                  "EX. $cf bl add channel general```" +
                                               "\nCongrats the chat filter is now set up on your server.\n" +
                                               "If you ever want to disable the filter, delete words, or channels use the following." +
                                               "```$cf disable\n" +
                                                  "$cf [wl, bl, rl] remove word <word>\n" +
                                                  "$cf [wl, bl, rl] remove channel <channel>```")

async def enable_chat_filter(message, client):
    user_permissions = message.author.server_permissions
    if user_permissions.administrator:
        server_id = message.server.id
        if os.path.exists(chat_filter_enable_path.format(server_id)):
            await client.send_message(message.channel, "The Chat Filter is already enabled.")
        elif os.path.exists(chat_filter_storage_path.format(server_id)):
            with open(chat_filter_enable_path.format(server_id), "w+") as file:
                file.writelines("enabled")
                file.close
            await client.send_message(message.channel, "The Chat Filter is now enabled.")
        else:
            os.makedirs(chat_filter_storage_path.format(server_id))
            with open(chat_filter_enable_path.format(server_id), "w+") as file:
                file.writelines("enabled")
                file.close
            await client.send_message(message.channel, "The Chat Filter is now enabled.")

    else:
        await client.send_message(message.author, "Sorry but you do not have access to '$cf enable' in {}.".format(message.server.name) +
                                                  "Please contact an administrator if this is wrong.")


async def disable_chat_filter(message, client):
    user_permissions = message.author.server_permissions
    if user_permissions.administrator:
        server_id = message.server.id
        if os.path.exists(chat_filter_enable_path.format(server_id)):
            os.remove(chat_filter_enable_path.format(server_id))
            await client.send_message(message.channel, "The Chat Filter is now disabled.")
        else:
            await client.send_message(message.channel, "The Chat Filter is already disabled.")

    else:
        await client.send_message(message.author, "Sorry but you do not hace access to '$cf disable' in {}.".format(message.server.name) +
                                                  "Please contact an administrator if this is wrong.")



async def add_word_to_blacklist(message, client, prefix):
    user_permissions = message.author.server_permissions
    if user_permissions.administrator:
        server_id = message.server.id
        new_word = message.content[15 + len(prefix):]
        conn = sqlite3.connect(chat_filter_config_path.format(server_id))
        c = conn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS blackListWords(blackListedWord TEXT)')
        c.execute("SELECT blackListedWord FROM blackListWords WHERE blackListedWord = (?)", (new_word,))
        for item in c.fetchall():
            for word in item:
                if word == new_word:
                    await client.send_message(message.channel, "The word '{}' has already been added to the BlackList.".format(new_word))
                    return
        c.execute("INSERT INTO blackListWords VALUES(?)", (new_word,))
        await client.send_message(message.channel, "The word '{}' has been added to the BlackList.".format(new_word))

        conn.commit()

        c.close()
        conn.close()

    else:
        await client.send_message(message.author, "Sorry but you do not have access to '$cf bl add word' in {}.".format(message.server.name) +
                                                  "Please contact an administrator if this is wrong.")


async def add_word_to_whitelist(message, client, prefix):
    user_permissions = message.author.server_permissions
    if user_permissions.administrator:
        server_id = message.server.id
        new_word = message.content[15 + len(prefix):]
        conn = sqlite3.connect(chat_filter_config_path.format(server_id))
        c = conn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS whiteListWords(whiteListedWord TEXT)')
        c.execute("SELECT whiteListedWord FROM whiteListWords WHERE whiteListedWord = (?)", (new_word,))
        for item in c.fetchall():
            for word in item:
                if word == new_word:
                    await client.send_message(message.channel, "The word '{}' has already been added to the WhiteList.".format(new_word))
                    return
        c.execute("INSERT INTO whiteListWords VALUES(?)", (new_word,))
        await client.send_message(message.channel, "The word '{}' has been added to the WhiteList.".format(new_word))

        conn.commit()

        c.close()
        conn.close()

    else:
        await client.send_message(message.author, "Sorry but you do not have access to '$cf wl add word' in {}.".format(message.server.name) +
                                                  "Please contact an administrator if this is wrong.")


async def add_word_to_redlist(message, client, prefix):
    user_permissions = message.author.server_permissions
    if user_permissions.administrator:
        server_id = message.server.id
        new_word = message.content[15 + len(prefix):]
        conn = sqlite3.connect(chat_filter_config_path.format(server_id))
        c = conn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS redListWords(redListedWord TEXT)')
        c.execute("SELECT redListedWord FROM redListWords WHERE redListedWord = (?)", (new_word,))
        for item in c.fetchall():
            for word in item:
                if word == new_word:
                    await client.send_message(message.channel, "The word '{}' has already been added to the RedList.".format(new_word))
                    return
        c.execute("INSERT INTO redListWords VALUES(?)", (new_word,))
        await client.send_message(message.channel, "The word '{}' has been added to the RedList.".format(new_word))

        conn.commit()

        c.close()
        conn.close()

    else:
        await client.send_message(message.author, "Sorry but you do not have access to '$cf rl add word' in {}.".format(message.server.name) +
                                                  "Please contact an administrator if this is wrong.")


async def add_channel_to_blacklist(message, client, prefix):
    user_permissions = message.author.server_permissions
    if user_permissions.administrator:
        server_id = message.server.id
        new_channel = message.content[18 + len(prefix):]
        conn = sqlite3.connect(chat_filter_config_path.format(server_id))
        c = conn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS blackListChannels(blackListChannel TEXT)')
        c.execute("SELECT blackListChannel FROM blackListChannels WHERE blackListChannel = (?)", (new_channel,))
        for item in c.fetchall():
            for channel in item:
                if channel == new_channel:
                    await client.send_message(message.channel, "The channel '{}' has already been added to the BlackList.".format(new_channel))
                    return
        c.execute("INSERT INTO blackListChannels VALUES(?)", (new_channel,))
        await client.send_message(message.channel, "The channel '{}' has been added to the BlackList.".format(new_channel))

        conn.commit()

        c.close()
        conn.close()

    else:
        await client.send_message(message.author, "Sorry but you do not have access to '$cf bl add channel' in {}.".format(message.server.name) +
                                                  "Please contact an administrator if this is wrong.")


async def add_channel_to_whitelist(message, client, prefix):
    user_permissions = message.author.server_permissions
    if user_permissions.administrator:
        server_id = message.server.id
        new_channel = message.content[18 + len(prefix):]
        conn = sqlite3.connect(chat_filter_config_path.format(server_id))
        c = conn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS whiteListChannels(whiteListChannel TEXT)')
        c.execute("SELECT whiteListChannel FROM whiteListChannels WHERE whiteListChannel = (?)", (new_channel,))
        for item in c.fetchall():
            for channel in item:
                if channel == new_channel:
                    await client.send_message(message.channel, "The channel '{}' has already been added to the WhiteList.".format(new_channel))
                    return
        c.execute("INSERT INTO whiteListChannels VALUES(?)", (new_channel,))
        await client.send_message(message.channel, "The channel '{}' has been added to the WhiteList.".format(new_channel))

        conn.commit()

        c.close()
        conn.close()

    else:
        await client.send_message(message.author, "Sorry but you do not have access to '$cf wl add channel' in {}.".format(message.server.name) +
                                                  "Please contact an administrator if this is wrong.")


async def add_channel_to_redlist(message, client, prefix):
    user_permissions = message.author.server_permissions
    if user_permissions.administrator:
        server_id = message.server.id
        new_channel = message.content[18 + len(prefix):]
        conn = sqlite3.connect(chat_filter_config_path.format(server_id))
        c = conn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS redListChannels(redListChannel TEXT)')
        c.execute("SELECT redListChannel FROM redListChannels WHERE redListChannel = (?)", (new_channel,))
        for item in c.fetchall():
            for channel in item:
                if channel == new_channel:
                    await client.send_message(message.channel, "The channel '{}' has already been added to the RedList.".format(new_channel))
                    return
        c.execute("INSERT INTO redListChannels VALUES(?)", (new_channel,))
        await client.send_message(message.channel, "The channel '{}' has been added to the RedList.".format(new_channel))

        conn.commit()

        c.close()
        conn.close()

    else:
        await client.send_message(message.author, "Sorry but you do not have access to '$cf rl add channel' in {}.".format(message.server.name) +
                                                  "Please contact an administrator if this is wrong.")

async def remove_word_from_blacklist(message, client, prefix):
    user_permissions = message.author.server_permissions
    if user_permissions.administrator:
        server_id = message.server.id
        word_to_remove = message.content[18 + len(prefix):]
        conn = sqlite3.connect(chat_filter_config_path.format(server_id))
        c = conn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS blackListWords(blackListedWord TEXT)')
        c.execute('DELETE FROM blackListWords WHERE blackListedWord = (?)', (word_to_remove,))

        conn.commit()

        c.close()
        conn.close()

        await client.send_message(message.channel , "The word '{}' has been removed from the BlackList.".format(word_to_remove))

    else:
        await client.send_message(message.author, "Sorry but you do not have access to '$cf bl remove word' in {}.".format(message.server.name) +
                                                  "Please contact an administrator if this is wrong.")


async def remove_word_from_whitelist(message, client, prefix):
    user_permissions = message.author.server_permissions
    if user_permissions.administrator:
        server_id = message.server.id
        word_to_remove = message.content[18 + len(prefix):]
        conn = sqlite3.connect(chat_filter_config_path.format(server_id))
        c = conn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS whiteListWords(whiteListedWord TEXT)')
        c.execute('DELETE FROM whiteListWords WHERE whiteListedWord = (?)', (word_to_remove,))

        conn.commit()

        c.close()
        conn.close()

        await client.send_message(message.channel , "The word '{}' has been removed from the WhiteList.".format(word_to_remove))

    else:
        await client.send_message(message.author, "Sorry but you do not have access to '$cf wl remove word' in {}.".format(message.server.name) +
                                                  "Please contact an administrator if this is wrong.")


async def remove_word_from_redlist(message, client, prefix):
    user_permissions = message.author.server_permissions
    if user_permissions.administrator:
        server_id = message.server.id
        word_to_remove = message.content[18 + len(prefix):]
        conn = sqlite3.connect(chat_filter_config_path.format(server_id))
        c = conn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS redListWords(redListedWord TEXT)')
        c.execute('DELETE FROM redListWords WHERE redListedWord = (?)', (word_to_remove,))

        conn.commit()

        c.close()
        conn.close()

        await client.send_message(message.channel , "The word '{}' has been removed from the RedList.".format(word_to_remove))

    else:
        await client.send_message(message.author, "Sorry but you do not have access to '$cf rl remove word' in {}.".format(message.server.name) +
                                                  "Please contact an administrator if this is wrong.")


async def remove_channel_from_blacklist(message, client, prefix):
    user_permissions = message.author.server_permissions
    if user_permissions.administrator:
        server_id = message.server.id
        channel_to_remove = message.content[21 + len(prefix):]
        conn = sqlite3.connect(chat_filter_config_path.format(server_id))
        c = conn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS blackListChannels(blackListChannel TEXT)')
        c.execute('DELETE FROM blackListChannels WHERE blackListChannel = (?)', (channel_to_remove,))

        conn.commit()

        c.close()
        conn.close()

        await client.send_message(message.channel , "The channel '{}' has been removed from the BlackList.".format(channel_to_remove))

    else:
        await client.send_message(message.author, "Sorry but you do not have access to '$cf bl remove channel' in {}.".format(message.server.name) +
                                                  "Please contact an administrator if this is wrong.")


async def remove_channel_from_whitelist(message, client, prefix):
    user_permissions = message.author.server_permissions
    if user_permissions.administrator:
        server_id = message.server.id
        channel_to_remove = message.content[21 + len(prefix):]
        conn = sqlite3.connect(chat_filter_config_path.format(server_id))
        c = conn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS whiteListChannels(whiteListChannel TEXT)')
        c.execute('DELETE FROM whiteListChannels WHERE whiteListChannel = (?)', (channel_to_remove,))

        conn.commit()

        c.close()
        conn.close()

        await client.send_message(message.channel , "The channel '{}' has been removed from the WhiteList.".format(channel_to_remove))

    else:
        await client.send_message(message.author, "Sorry but you do not have access to '$cf wl remove channel' in {}.".format(message.server.name) +
                                                  "Please contact an administrator if this is wrong.")


async def remove_channel_from_redlist(message, client, prefix):
    user_permissions = message.author.server_permissions
    if user_permissions.administrator:
        server_id = message.server.id
        channel_to_remove = message.content[21 + len(prefix):]
        conn = sqlite3.connect(chat_filter_config_path.format(server_id))
        c = conn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS redListChannels(redListChannel TEXT)')
        c.execute('DELETE FROM redListChannels WHERE redListChannel = (?)', (channel_to_remove,))

        conn.commit()

        c.close()
        conn.close()

        await client.send_message(message.channel , "The channel '{}' has been removed from the RedList.".format(channel_to_remove))

    else:
        await client.send_message(message.author, "Sorry but you do not have access to '$cf rl remove channel' in {}.".format(message.server.name) +
                                                  "Please contact an administrator if this is wrong.")



async def blacklist_checker(message, client):
    server_id = message.server.id
    conn = sqlite3.connect(chat_filter_config_path.format(server_id))
    c = conn.cursor()

    try:
        c.execute("SELECT blackListChannel from blackListChannels WHERE blackListChannel = (?)", (message.channel.name,))
    except:
        return
    else:
        for item in c.fetchall():
            for channel in item:
                if channel == message.channel.name:
                    c.execute("SELECT blackListedWord from blackListWords")
                    for thing in c.fetchall():
                        for word in thing:
                            for word_to_check in message.content.lower().split(" "):
                                word_to_check = word_to_check.replace("?", "").replace(",", "").replace(".", "").replace("\"", "").replace("'", "").replace("!", "").replace("@", "").replace("#", "")
                                word_to_check = word_to_check.replace("$", "").replace("%", "").replace("^", "").replace("&", "").replace("*", "").replace("(", "").replace(")", "").replace("-", "")
                                word_to_check = word_to_check.replace("_", "").replace("=", "").replace("+", "").replace("[", "").replace("]", "").replace("\\", "").replace("|", "").replace(";", "")
                                word_to_check = word_to_check.replace(":", "").replace("`", "").replace("~", "")
                                if word_to_check == word:
                                    try:
                                        await client.delete_message(message)
                                    except discord.HTTPException:
                                        return
                                    except:
                                        await client.send_message(message.server.owner, "I do not have the appropriate permissions to delete messages in {} when I filter with the ChatFilter.".format(message.server.name))
                                    else:
                                        await client.send_message(message.author, "You have used a BlackListed word in {}, please refrain from using them.".format(message.server.name))
                                    c.close()
                                    conn.close()
                                    return
    c.close()
    conn.close()


async def whitelist_checker(message, client):
    server_id = message.server.id
    conn = sqlite3.connect(chat_filter_config_path.format(server_id))
    c = conn.cursor()

    try:
        c.execute("SELECT whiteListChannel from whiteListChannels WHERE whiteListChannel = (?)", (message.channel.name,))
    except:
        return
    else:
        for item in c.fetchall():
            for channel in item:
                if channel == message.channel.name:
                    c.execute("SELECT whiteListedWord from whiteListWords")
                    for thing in c.fetchall():
                        for word in thing:
                            for word_to_check in message.content.lower().split(" "):
                                if word_to_check == word:
                                    c.close()
                                    conn.close()
                                    return
                    try:
                        await client.delete_message(message)
                    except discord.HTTPException:
                        return
                    except:
                        await client.send_message(message.server.owner, "I do not have the appropriate permissions to delete messages in {} when I filter with the ChatFilter.".format(message.server.name))
                    else:
                        await client.send_message(message.author, "You have not used a WhiteListed word in {}, please use one in order to talk.".format(message.server.name))
    c.close()
    conn.close()


async def redlist_checker(message, client):
    server_id = message.server.id
    conn = sqlite3.connect(chat_filter_config_path.format(server_id))
    c = conn.cursor()

    try:
        c.execute("SELECT redListChannel from redListChannels WHERE redListChannel = (?)", (message.channel.name,))
    except:
        return
    else:
        for item in c.fetchall():
            for channel in item:
                if channel == message.channel.name:
                    c.execute("SELECT redListedWord from redListWords")
                    for thing in c.fetchall():
                        for word in thing:
                            if word in message.content.lower() and word != "":
                                try:
                                    await client.delete_message(message)
                                except discord.HTTPException:
                                    return
                                except:
                                    await client.send_message(message.server.owner, "I do not have the appropriate permissions to delete messages in {} when I filter with the ChatFilter.".format(message.server.name))
                                else:
                                    await client.send_message(message.author, "You have used a RedListed phrase in {}, please refrain from using them.".format(message.server.name))
                                c.close()
                                conn.close()
                                return
    c.close()
    conn.close()
