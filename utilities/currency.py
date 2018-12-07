import sqlite3
import schedule
import time
import os
import random
from constants import coin_storage_path
from constants import daily_miner_path
from constants import weekly_miner_path

async def start_mining(message, client):
    # Connect to the DB
    conn = sqlite3.connect(coin_storage_path)
    c = conn.cursor()
    user_id = message.author.id
    c.execute('CREATE TABLE IF NOT EXISTS userCurrencyInfo(userID TEXT, tier INTEGER, balance INTEGER)')
    # Check if already in table
    c.execute('SELECT userID FROM userCurrencyInfo WHERE userID = (?)', (user_id,))
    for item in c.fetchall():
        for thing in item:
            if thing == user_id:
                await client.send_message(message.channel, "{}, you have already started mining Legacy Coins.".format(message.author.display_name))
                c.close()
                conn.close()
                return
    # Insert into  table, ID / Tier / Balance
    c.execute("INSERT INTO userCurrencyInfo VALUES((?), 1, 0)", (user_id,))
    await client.send_message(message.channel, "{}, you are now mining Legacy Coins.".format(message.author.display_name))
    conn.commit()
    c.close()
    conn.close()


def check_if_mining(user_id, conn, c):
    c.execute("SELECT userID FROM userCurrencyInfo WHERE userID = (?)", (user_id,))
    for item in c.fetchall():
        for thing in item:
            if thing == user_id:
                return True
    return False


def get_coin_amount(user_id, conn, c):
    c.execute("SELECT balance FROM userCurrencyInfo WHERE userID = (?)", (user_id,))
    for item in c.fetchall():
        for thing in item:
            return thing


def update_coin_amount(user_id, coins, conn, c):
    current_coins = get_coin_amount(user_id, conn, c)
    new_coin_amount = current_coins + coins
    c.execute("UPDATE userCurrencyInfo SET balance = (?) WHERE userID = (?)", (new_coin_amount, user_id))
    conn.commit()
    return new_coin_amount


def check_daily_mining(user_id, conn, c):
    daily = sqlite3.connect(daily_miner_path)
    d = daily.cursor()
    d.execute('CREATE TABLE IF NOT EXISTS dailyCoinUser(userID TEXT)')
    d.execute("SELECT userID FROM dailyCoinUser WHERE userID = (?)", (user_id,))
    for item in d.fetchall():
        for thing in item:
            if thing == user_id:
                d.close()
                daily.close()
                return True
    d.execute("INSERT INTO dailyCoinUser VALUES((?))", (user_id,))
    daily.commit()
    d.close()
    daily.close()
    return False


def check_weekly_mining(user_id, conn, c):
    weekly = sqlite3.connect(weekly_miner_path)
    w = weekly.cursor()
    w.execute('CREATE TABLE IF NOT EXISTS weeklyCoinUser(userID TEXT)')
    w.execute("SELECT userID FROM weeklyCoinUser WHERE userID = (?)", (user_id,))
    for item in w.fetchall():
        for thing in item:
            if thing == user_id:
                w.close()
                weekly.close()
                return True
    w.execute("INSERT INTO weeklyCoinUser VALUES((?))", (user_id,))
    weekly.commit()
    w.close()
    weekly.close()
    return False


async def get_user_balance(message, client):
    # Connect to the DB
    conn = sqlite3.connect(coin_storage_path)
    c = conn.cursor()
    user_id = message.author.id
    # Check if trying to get balance of other user
    if len(message.mentions) >= 1:
        # Check if mentioned user's is mining
        user_to_check_id = message.mentions[0].id
        if check_if_mining(user_to_check_id, conn, c) == True:
            # If They are mining get balance
            current_balance = get_coin_amount(user_to_check_id, conn, c)
            # Return User Balance
            await client.send_message(message.channel, "{} currently has {} Legacy Coins.".format(message.mentions[0].display_name, current_balance))
        else:
            await client.send_message(message.channel, "{} has not started mining Legacy Coins.".format(message.mentions[0].display_name))
    else:
        # Check if User is mining or not
        if check_if_mining(user_id, conn, c) == True:
            # if they are mining get balance
            current_balance = get_coin_amount(user_id, conn, c)
            # Return user balance
            await client.send_message(message.channel, "You currently have {} Legacy Coins.".format(current_balance))
        else:
            await client.send_message(message.channel, "You have not started mining Legacy Coins, use '$lc start' to get started.")
    c.close()
    conn.close()


async def get_daily_coins(message, client):
    # Connect to the DB
    conn = sqlite3.connect(coin_storage_path)
    c = conn.cursor()
    user_id = message.author.id
    # Check if User is mining or not
    if check_if_mining(user_id, conn, c) == True:
        # If mining, Check if already collected
        if check_daily_mining(user_id, conn, c) == True:
            await client.send_message(message.channel, "{}, you have already collected your daily coins.".format(message.author.display_name))
        # If Not collected, add 100 coins to user
        else:
            # Return New Balance
            new_coin_amount = update_coin_amount(user_id, 100, conn, c)
            await client.send_message(message.channel, "{}, you have collected your daily coins and your new amount is {}.".format(message.author.display_name, new_coin_amount))
    else:
        await client.send_message(message.channel, "You have not started mining Legacy Coins, use '$lc start' to get started.")
    c.close()
    conn.close()


async def get_weekly_coins(message, client):
    # Connect to the DB
    conn = sqlite3.connect(coin_storage_path)
    c = conn.cursor()
    user_id = message.author.id
    # Check if User is mining or Not
    if check_if_mining(user_id, conn, c) == True:
        # IF mining, Check if already mined
        if check_weekly_mining(user_id, conn, c) == True:
            await client.send_message(message.channel, "{}, you have already collected your weekly coins.".format(message.author.display_name))
        # If Not mined, add 500 coins to user
        else:
            # Return New Balance
            new_coin_amount = update_coin_amount(user_id, 500, conn, c)
            await client.send_message(message.channel, "{}, you have collected your weekly coins and your new amount is {}.".format(message.author.display_name, new_coin_amount))
    else:
        await client.send_message(message.channel, "You have not started mining Legacy Coins, use '$lc start' to get started.")
    c.close()
    conn.close()


async def gamble_coins(message, client):
    # Connect to the DB
    conn = sqlite3.connect(coin_storage_path)
    c = conn.cursor()
    user_id = message.author.id
    # Check if mining
    if check_if_mining(user_id, conn, c) == True:
        # Check if actually entered a real coin amount
        coins_to_gamble = message.content.split(" ")[2]
        try:
            coins_to_gamble = int(coins_to_gamble)
        except:
            await client.send_message(message.channel, "{}, you have not entered an actual amount of coins to gamble.".format(message.author.display_name))
        else:
            # If mining See if they have enough coins
            user_coin_amount = get_coin_amount(user_id, conn, c)
            if user_coin_amount >= coins_to_gamble:
                # Check if gamble multiplier is a real multiplier
                multiplier = message.content.split(" ")[3]
                try:
                    multiplier = float(multiplier)
                except:
                    await client.send_message(message.channel, "{}, you have not entered an actual multiplier to gamble with.".format(message.author.display_name))
                else:
                    # If have enough coins and multiplier is real gamble them
                    winning_range = 100 / multiplier
                    user_random_num = random.randint(1, 100)
                    if user_random_num < winning_range:
                        # If won, add coins to current coins, return balance.
                        coins_to_add = int(coins_to_gamble * multiplier) - coins_to_gamble
                        update_coin_amount(user_id, coins_to_add, conn, c)
                        new_balance = get_coin_amount(user_id, conn, c)
                        await client.send_message(message.channel, "{}, congrats you have won the gamble! Your new balance of coins is {}.".format(message.author.display_name, new_balance))
                    else:
                        # If lost, Subtract coins lost, return balance
                        update_coin_amount(user_id, coins_to_gamble * -1, conn, c)
                        new_balance = user_coin_amount - coins_to_gamble
                        await client.send_message(message.channel, "{}, sorry but you have lost! Your new balance of coins is {}.".format(message.author.display_name, new_balance))
            else:
                await client.send_message(message.channel, "{}, sorry but you are trying to gamble with more coins than you have! You only have {}.".format(message.author.display_name, user_coin_amount))
    else:
        await client.send_message(message.channel, "You have not started mining Legacy Coins, use '$lc start' to get started.")
    c.close()
    conn.close()


async def pay_coins(message, client):
    # Connect to DB
    conn = sqlite3.connect(coin_storage_path)
    c = conn.cursor()
    payer_id = message.author.id
    # Check if user is mining
    if check_if_mining(payer_id, conn, c) == True:
        # If user is mining, check if person getting payed is mining
        payed_user_id = message.mentions[0].id
        if check_if_mining(payed_user_id, conn, c) == True:
            # If person getting payed is also mining, check if payment is a realy number
            pay_amount = message.content.split(" ")[3]
            try:
                pay_amount = int(pay_amount)
            except:
                await client.send_message(message.channel, "{}, you have not entered a valid payment amount.".format(message.author.display_name))
            else:
                # If payment is a real number, check if they have enough pay
                current_payer_balance = get_coin_amount(payer_id, conn, c)
                if current_payer_balance >= pay_amount:
                    # If payer has enough money to pay, pay user
                    update_coin_amount(payer_id, pay_amount * -1, conn, c)
                    update_coin_amount(payed_user_id, pay_amount, conn, c)
                    # Return current balance to payer, and send a private message to payed user
                    payer_new_balance = get_coin_amount(payer_id, conn, c)
                    await client.send_message(message.channel, "{}, you have payed {} {} Legacy Coins, and your current balance is now {}.".format(message.author.display_name, message.mentions[0].display_name, pay_amount, payer_new_balance))
                    payed_user_balance = get_coin_amount(payed_user_id, conn, c)
                    try:
                        await client.send_message(message.mentions[0], "{} has payed you {} Legacy Coins, and your current balance is now {}.".format(message.author.display_name, pay_amount, payed_user_balance))
                    except:
                        print("Could not message payed user.")
                else:
                    await client.send_message(message.channel, "{}, sorry but you do not have enough coins to pay {}. You only have {}.".format(message.author.display_name, message.mentions[0].display_name, current_payer_balance))
        else:
            await client.send_message(message.channel, "{}, sorry but {} has not started mining Legacy Coins yet so they cannot receive them. Tell them to start mining by saying '$lc start'.".format(message.author.display_name, message.mentions[0].display_name))
    else:
        await client.send_message(message.channel, "You have not started mining Legacy Coins, use '$lc start' to get started.")
    c.close()
    conn.close()


async def global_leaderboard(message, client):
    # Get page number selected
    if message.content[7:] != "" and message.content[7:] != " ":
        try:
            page_number = int(message.content[8:])
        except:
            await client.send_message(message.channel, "{}, you have not entered a valid page number.".format(message.author.display_name))
            return
    else:
        # Connect to DB
        conn = sqlite3.connect(coin_storage_path)
        c = conn.cursor()
        page_number = 1
        # If it is a real number, select both the ID and Balance of the Users
        c.execute("SELECT userID, balance FROM userCurrencyInfo ORDER BY balance DESC")
        data = c.fetchall()
        number_to_start_at = page_number * 5 - 5
        # Check if there is enough people for that page
        if len(data) - 1 >= number_to_start_at:
            # If there is return the 5 users for that page
            msg = "**Legacy Coins Leaderboard**" + "```"
            i = 1
            while True:
                try:
                    user = await client.get_user_info(data[number_to_start_at + i - 1][0])
                    msg = msg + "{}. {} - {} Coins\n".format(number_to_start_at + i, user, data[number_to_start_at + i - 1][1])
                except:
                    break
                else:
                    i += 1
                    if i > 5:
                        break
            msg = msg + "\n" + "Page {} of {}```".format(page_number, ((int(len(data) / 5)) if len(data) % 5 == 0 else (int(len(data) / 5) + 1)))
            await client.send_message(message.channel, msg)
        else:
            await client.send_message(message.channel, "{}, you have entered too high of a page number. The highest page is {}.".format(message.author.display_name, ((int(len(data) / 5)) if len(data) % 5 == 0 else (int(len(data) / 5) + 1))))
    c.close()
    conn.close()
