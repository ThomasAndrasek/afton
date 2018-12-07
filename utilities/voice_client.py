from __future__ import unicode_literals
from constants import pafy_key
from constants import song_queue_path
from constants import completed_skip_path
from constants import voting_skip_path
from constants import completed_stop_path
from constants import voting_stop_path
import urllib.request
import urllib.parse
import re
import asyncio
import os
import pafy
import discord

pafy.set_api_key(pafy_key)

async def play(message, client, player):
    server_id = message.server.id
    link_to_try = message.content[6:]
    if os.path.exists(song_queue_path.format(server_id)):
        voice = message.server.voice_client
        if message.author.voice.voice_channel != voice.channel:
            await client.send_message(message.channel, "You must be in the voice channel with the bot to request songs.")
        else:
            try:
                myvid = pafy.new(link_to_try)
            except:
                query_string = urllib.parse.urlencode({"search_query" : link_to_try})
                html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
                search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
                link_to_try = "http://www.youtube.com/watch?v=" + search_results[0]
                myvid = pafy.new(link_to_try)
            finally:
                current_queue = open(song_queue_path.format(server_id)).readlines()[0]
                current_queue = current_queue.replace("'", "").replace("[", "").replace("]", "")
                with open(song_queue_path.format(server_id), "w") as file:
                    file.writelines("{}{} ".format(current_queue, link_to_try))
                    file.close()
                await client.send_message(message.channel, "Added to the queue >> {}".format(myvid.title))
    else:
        try:
            await client.join_voice_channel(message.author.voice.voice_channel)
        except discord.InvalidArgument:
            await client.send_message(message.channel, "You are not in a voice channel.")
        except asyncio.TimeoutError:
            await client.send_message(message.channel, "Either the voice channel is full, or I do not have the appropriate permissions.")
        else:
            try:
                voice = message.server.voice_client
                player = await voice.create_ytdl_player(link_to_try)
            except:
                query_string = urllib.parse.urlencode({"search_query" : link_to_try})
                html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
                search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
                link_to_try = "http://www.youtube.com/watch?v=" + search_results[0]
                player = await voice.create_ytdl_player(link_to_try)
            finally:
                with open(song_queue_path.format(server_id), "w+") as file:
                    file.writelines("{} ".format(link_to_try))
                    file.close
                player.start()
                await client.send_message(message.channel, "Now playing >> {}".format(player.title))
        return player

async def queue(message, client):
    #Get Server Id
    song_page = ""
    server_id = message.server.id
    #Check for song queue file
    if os.path.exists(song_queue_path.format(server_id)):
        if message.content[6:] != "" and message.content[6:] != " ":
            try:
                page_num = int(message.content[7:])
            except:
                await client.send_message(message.channel, "You have not entered a vaild page number for the queue.")
                return

        else:
            page_num = 1

        with open(song_queue_path.format(server_id), "r") as file:
            data = file.readlines()
            file.close

        song_queue = data[0].split(" ")
        if int(len(song_queue) / 5) + 1 < page_num or page_num < 1:
            await client.send_message(message.channel, "You have not entered a valid page number for the queue.")
            return

        song_limit = 5 * page_num
        song = song_limit - 5

        while song < song_limit:
            try:
                my_song = pafy.new(song_queue[song])
                song_page = song_page + "{}.{} - {}\n\n".format((song + 1), my_song.title, my_song.duration)
            except:
                break
            song += 1

        await client.send_message(message.channel, "Current song queue." +
                                                   "```{}```\n".format(song_page) +
                                                   "Page {} of {}.".format(page_num, (int(len(song_queue) / 5) + 1)))

    else:
        await client.send_message(message.channel, "There is no music in queue right now.")



    #If it exists return five songs from the list
    #If user does not specify page default page 1
    #Tell how many pages of queue

async def skip(message, client):
    server_id = message.server.id
    user_permissions = message.author.server_permissions
    voice = message.server.voice_client
    if message.author.voice.voice_channel == voice.channel:
        if user_permissions.administrator:
            with open(completed_skip_path.format(server_id), "w+") as file:
                file.writelines("done")
                file.close

            if os.path.exists(voting_skip_path.format(server_id)):
                os.remove(voting_skip_path.format(server_id))

            await client.send_message(message.channel, "Skipping...")

        else:
            user_id = message.author.id
            voice = message.server.voice_client
            amount_of_people = len(voice.channel.voice_members)

            if os.path.exists(voting_skip_path.format(server_id)):
                with open(voting_skip_path.format(server_id), "r") as file:
                    votes = file.readlines()
                    file.close

                for vote in votes:
                    if user_id not in vote:
                        continue
                    else:
                        await client.send_message(message.channel, "{}, you have already voted.".format(message.author.display_name))
                        return

                total_votes = len(votes) + 1

                if total_votes / amount_of_people >= 0.5:
                    os.remove(voting_skip_path.format(server_id))

                    with open(completed_skip_path.format(server_id), "w+") as file:
                        file.writelines("done")
                        file.close

                    await client.send_message(message.channel, "Skipping...")

                else:
                    with open(voting_skip_path.format(server_id), "w") as file:
                        file.writelines("{}\n{}".format(votes, user_id))
                        file.close

                    await client.send_message(message.channel, "{} out of {} votes to skip.".format(len(votes) + 1, ((int(amount_of_people / 2)) if amount_of_people % 2 == 0 else (int(amount_of_people / 2 + 0.5)))))

            else:
                if 1 / amount_of_people >= 0.5:
                    with open(completed_skip_path.format(server_id), "w+") as file:
                        file.writelines("done")
                        file.close

                    await client.send_message(message.channel, "Skipping...")
                else:
                    with open(voting_skip_path.format(server_id), "w+") as file:
                        file.writelines("{}".format(user_id))
                        file.close

                    await client.send_message(message.channel, "1 out of {} votes to skip.".format(((int(amount_of_people / 2)) if amount_of_people % 2 == 0 else (int(amount_of_people / 2 + 0.5)))))
    else:
        await client.send_message(message.channel, "You must be in the voice channel with the bot to skip songs.")


async def stop(message, client):
    server_id = message.server.id
    user_permissions = message.author.server_permissions
    voice = message.server.voice_client
    if message.author.voice.voice_channel == voice.channel:
        if user_permissions.administrator:
            with open(completed_stop_path.format(server_id), "w+") as file:
                file.writelines("done")
                file.close

            if os.path.exists(voting_stop_path.format(server_id)):
                os.remove(voting_stop_path.format(server_id))

            await client.send_message(message.channel, "Stopping...")

        else:
            user_id = message.author.id
            voice = message.server.voice_client
            amount_of_people = len(voice.channel.voice_members)

            if os.path.exists(voting_stop_path.format(server_id)):
                with open(voting_stop_path.format(server_id), "r") as file:
                    votes = file.readlines()
                    file.close

                for vote in votes:
                    if user_id not in vote:
                        continue
                    else:
                        await client.send_message(message.channel, "{}, you have already voted.".format(message.author.display_name))
                        return

                total_votes = len(votes) + 1

                if total_votes / amount_of_people >= 0.5:
                    os.remove(voting_stop_path.format(server_id))

                    with open(completed_stop_path.format(server_id), "w+") as file:
                        file.writelines("done")
                        file.close

                    await client.send_message(message.channel, "Stopping...")

                else:
                    with open(voting_stop_path.format(server_id), "w") as file:
                        file.writelines("{}\n{}".format(votes, user_id))
                        file.close

                    await client.send_message(message.channel, "{} out of {} votes to stop.".format(len(votes) + 1, ((int(amount_of_people / 2)) if amount_of_people % 2 == 0 else (int(amount_of_people / 2 + 0.5)))))

            else:
                if 1 / amount_of_people >= 0.5:
                    with open(completed_stop_path.format(server_id), "w+") as file:
                        file.writelines("done")
                        file.close

                    await client.send_message(message.channel, "Stopping...")
                else:
                    with open(voting_stop_path.format(server_id), "w+") as file:
                        file.writelines("{}".format(user_id))
                        file.close

                    await client.send_message(message.channel, "1 out of {} votes to stop.".format(((int(amount_of_people / 2)) if amount_of_people % 2 == 0 else (int(amount_of_people / 2 + 0.5)))))
    else:
        await client.send_message(message.channel, "You must be in the voice channel with the bot to stop songs.")


async def voice_player(message, client, player):
    voice = message.server.voice_client
    server_id = message.server.id
    while True:
        if os.path.exists(completed_skip_path.format(server_id)):
            player.stop()
            os.remove(completed_skip_path.format(server_id))

        if os.path.exists(completed_stop_path.format(server_id)):
            player.stop()
            os.remove(completed_stop_path.format(server_id))
            os.remove(song_queue_path.format(server_id))
            if os.path.exists(voting_skip_path.format(server_id)):
                os.remove(voting_skip_path.format(server_id))
            await voice.disconnect()
            break

        if player.is_playing() != True:
            if os.path.exists(voting_skip_path.format(server_id)):
                os.remove(voting_skip_path.format(server_id))
            current_queue = open(song_queue_path.format(server_id)).readlines()[0]
            current_queue = current_queue.replace("'", "").replace("[", "").replace("]", "")
            current_queue = current_queue[current_queue.index("h"):]
            song_list = current_queue.split(" ")
            song_list = song_list[:len(song_list) - 1]
            if len(song_list) > 1:
                next_song = song_list[1]
                player = await voice.create_ytdl_player(next_song)
                player.start()
                new_song_queue = current_queue[current_queue.index(" "):]
                with open(song_queue_path.format(server_id), "w+") as file:
                    file.writelines("{}".format(new_song_queue))
                    file.close
                await client.send_message(message.channel, "Now playing >> {}".format(player.title))
            else:
                await client.send_message(message.channel, "Queue concluded")
                await voice.disconnect()
                os.remove(song_queue_path.format(server_id))
                break

        if len(voice.channel.voice_members) == 1:
            await client.send_message(message.channel, "All users have left voice channel. Ending queue.")
            await voice.disconnect()
            os.remove(song_queue_path.format(server_id))
            break
        await asyncio.sleep(1)
