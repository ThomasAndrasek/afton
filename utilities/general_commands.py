import random
import discord

async def invite(message, client):
    if message.channel.is_private != True:
        await client.send_message(message.channel, "I am private messaging you an invite code for the bot.")

    await client.send_message(message.author, "Thank you for considering to invite me to your server, I am always here to help!\n" +
                                               "https://discordapp.com/oauth2/authorize?client_id=385206243779674132&permissions=53963847&scope=bot")

async def vote(message, client):
    if message.channel.is_private != True:
        await client.send_message(message.channel, "I am private messaging you a link to vote.")

    await client.send_message(message.author, "Thank you so much for considering to vote, it is the best way to support me at the moment!\n" +
                                               "https://discordbots.org/bot/385206243779674132/vote")

async def hello(message, client):
    await client.send_message(message.channel, "Hello {}, I am Afton, your personal Discord assistant.".format(message.author.display_name))

async def love(message, client, prefix):
    loved_thing = message.content[5 + len(prefix):]
    amount_of_love = random.randint(1, 100)
    await client.send_message(message.channel, "There is a {}% love between {} and {}.".format(amount_of_love, message.author.display_name, loved_thing))

async def coinflip(message, client):
    heads = random.randint(0, 1)
    if heads == 1: await client.send_message(message.channel, "Heads")
    else: await client.send_message(message.channel, "Tails")

async def roll_dice(message, client, prefix):
    rolled_dice = ""
    if message.content[8 + len(prefix):] != "" and message.content[9:] != " ":
        try:
            num_of_dice = int(message.content[9 + len(prefix):])
            if num_of_dice > 100:
                num_of_dice = 100
        except:
            await client.send_message(message.channel, "You do not enter a valid number of dice.")
            return
    else:
        num_of_dice = 1

    num_of_dice_rolled = 0

    while num_of_dice_rolled < num_of_dice:
        rolled_dice = rolled_dice + "{} ".format(random.randint(1, 6))
        num_of_dice_rolled += 1

    await client.send_message(message.channel, "I have rolled. ```{}```".format(rolled_dice))

async def support(message, client, prefix):
    await client.send_message(message.author, "**Hello, I am Afton, your personal Discord assistant.**\n" +
                                             "Here are all the current commands you can use.\n" +
                                             "On this server I respond to '{}'\n".format(prefix) +
                                             "**Want to invite me to your server?**" +
                                             "```{}invite```".format(prefix) +
                                             "**Want to support me on my adventure?**" +
                                             "```{}vote```".format(prefix) +
                                             "__General Commands__" +
                                             "```{}help\n".format(prefix) +
                                                "{}love <something>\n".format(prefix) +
                                                "{}coinflip\n".format(prefix) +
                                                "{}8ball\n".format(prefix) +
                                                "{}rolldice <amount>\n".format(prefix) +
                                                "{}servercount\n".format(prefix) +
                                                "{}serverinfo\n".format(prefix) +
                                                "{}userinfo @user".format(prefix) +
                                                "{}prefix <prefix>```".format(prefix) +
                                             "__ChatFilter Commands__" +
                                             "```{}cf help\n".format(prefix) +
                                                "{}cf enable/disable\n".format(prefix) +
                                                "{}cf [wl, rl, bl] add word <word>\n".format(prefix) +
                                                "{}cf [wl, rl, bl] add channel <channel>\n".format(prefix) +
                                                "{}cf [wl, rl, bl] remove word <word>\n".format(prefix) +
                                                "{}cf [wl, rl, bl] remove channel <channel>\n".format(prefix) +
                                                "Use wl for WhiteList, bl for BlackList, rl for RedList.```")

async def server_count(message, client):
    amount_of_servers = len(client.servers)
    await client.send_message(message.channel, "I am connected to {} servers.".format(amount_of_servers))

async def server_info(message, client):
    if message.channel.is_private != True:
        server = message.server
        server_region = server.region
        server_name = server.name
        server_id = server.id
        server_emojis = server.emojis
        server_afk_timeout = server.afk_timeout
        server_afk_channel = server.afk_channel
        server_member_count = server.member_count
        server_icon = server.icon_url
        server_owner = server.owner
        server_verification_level = server.verification_level
        server_mfa_level = server.mfa_level
        server_features = server.features
        server_creation_date = server.created_at

        em = discord.Embed(title='{} Info'.format(server_name), description='Basic info of the server.', color=0x226be2)
        em.set_author(name=server_owner, icon_url=server_owner.avatar_url)
        em.add_field(name='Server Name', value=server_name, inline=True)
        em.add_field(name='Server Owner', value=server_owner, inline=True)
        em.add_field(name='Server ID', value=server_id, inline=True)
        em.add_field(name='Server Region', value=server_region, inline=True)
        em.add_field(name='Creation Date UTC', value=str(server_creation_date)[:-7], inline=True)
        em.add_field(name='Member Count', value=server_member_count, inline=True)
        em.add_field(name='AFK Channel', value=server_afk_channel, inline=True)
        em.add_field(name='AFK Timeout Time', value=server_afk_timeout, inline=True)
        em.add_field(name='Verification Level', value=server_verification_level, inline=True)
        em.add_field(name='MFA Level', value=server_mfa_level, inline=True)
        em.add_field(name='Special Server Features', value=server_features, inline=False)
        em.add_field(name='Server Emojis', value="All in reactions", inline=False)
        em.set_thumbnail(url=server_icon)

        message = await client.send_message(message.channel, embed=em)
        for emoji in server_emojis:
            await client.add_reaction(message, emoji)
    else:
        await client.send_message(message.channel, "Sorry, but this command must be used in a server.")

async def user_info(message, client):
    if message.channel.is_private != True:
        server = message.server
        member = message.mentions[0]
        user_name = member.name
        user_id = member.id
        user_avatar = member.avatar_url
        user_bot = member.bot
        user_creation = member.created_at
        user_display_name = member.display_name
        user_join_server_date = member.joined_at
        user_roles = member.roles
        user_status = member.status
        user_game = member.game
        user_top_role = member.top_role
        em = discord.Embed(title='{} Info'.format(user_name), description='Basic info of the user.', color=0x226be2)
        em.set_author(name=user_name, icon_url=user_avatar)
        em.add_field(name='User Name', value=user_name, inline=True)
        em.add_field(name='User ID', value=user_id, inline=True)
        em.add_field(name='User Display Name', value=user_display_name, inline=True)
        em.add_field(name='User Bot', value=user_bot, inline=True)
        em.add_field(name='User Creation', value=str(user_creation)[:-7], inline=True)
        em.add_field(name='User Status', value=user_status, inline=True)
        em.add_field(name='User Game', value=user_game, inline=True)
        em.add_field(name='User Joined Server At', value=str(user_join_server_date)[:-7], inline=True)
        em.add_field(name='User Top Server Role', value=user_top_role, inline=True)
        em.set_thumbnail(url=user_avatar)

        await client.send_message(message.channel, embed=em)
    else:
        await client.send_message(message.channel, "Sorry, but this command must be used in a server.")


async def eight_ball(message, client):
    eight_ball_answers = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes",
                          "Reply hazy try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
                          "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]
    #Generate a random number for the length of the list
    eight_ball_answer = random.randint(0, len(eight_ball_answers) - 1)
    #Return the specified list number based off random number
    await client.send_message(message.channel, "{}, {}".format(message.author.display_name, eight_ball_answers[eight_ball_answer]))
