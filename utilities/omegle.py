import os

def create_chat(id_one, id_two):
    os.makedirs("C:\\Users\\kille\\Desktop\\work space\\Afton\\Omegle\\Chats\\{}-{}".format(id_one, id_two))
    os.remove("C:\\Users\\kille\\Desktop\\work space\\Afton\\Omegle\\Searching\\{}".format(id_one))
    os.remove("C:\\Users\\kille\\Desktop\\work space\\Afton\\Omegle\\Searching\\{}".format(id_two))

async def search_person(message, client):
    with open("C:\\Users\\kille\\Desktop\\work space\\Afton\\Omegle\\Searching\\{}".format(message.author.id), + "w+") as file:
        file.writelines("searching")
        file.close()

    await client.send_message(message.author, "Searching...")

    if len(os.listdirs("C:\\Users\\kille\\Desktop\\work space\\Afton\\Omegle\\Searching")) > 1:
        create_chat(message.author.id, os.listdirs[1])
        await client.send_message(message.author, "You are connected to a random stranger!")
        user = await client.get_user_info(os.listdirs[])
        await client.send_message(user, "You are connected to a random stranger!")
