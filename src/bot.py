import discord
import random
import logging
import string
import database

START_ZOOMCORD_COMMAND = '!zoomcord'
WEBAPP_URL = 'https://example.com'
PAIR_ID_LENGTH = 5

client = None

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.content.startswith(START_ZOOMCORD_COMMAND):
            user_id = message.author.id
            pair_id = database.get_pair_id_from_user_id(user_id)
            if pair_id is None:
                pair_id = generate_random_pair_id(PAIR_ID_LENGTH)
                database.store_pair_data(pair_id, message.author.id)
            store_discord_data(message)

            await send_pair_dm(message.author, pair_id)

    async def punish(user_data):
        split_punishments = user_data.punishments.split(',')
        punishment = random.choices(split_punishments)
        if punishment == 'angry_message':
            await send_angry_message(user_data.user_id)

async def send_pair_dm(user, pair_id):
    print(f'Sending pair message to {user.name}')
    message = f'Welcome to Zoomcord, {user.name}! Please go to {WEBAPP_URL} and input the code {pair_id}'
    send_dm(user, message)


ANGRY_MESSAGES = ['You call that zooming?',
                  'You are a disgrace to Discord users everywhere.',
                  'I bet you use light mode',
                  'How slow can you possibly go? Get moving!']


async def send_angry_message(user):
    message = random.choice(ANGRY_MESSAGES)
    send_dm(user, message)

async def send_dm(user, message):
    dm_channel = user.dm_channel
    if dm_channel is None:
        dm_channel = await user.create_dm()
    await dm_channel.send(message)


LETTERS_AND_DIGITS = string.ascii_uppercase + string.digits
PAIR_ID_GENERATE_TRIES = 5


def generate_random_pair_id(length):
    for i in range(5):
        pair_id = ''.join(random.choice(LETTERS_AND_DIGITS) for _ in range(length))
        if database.get_user_id_from_pair_id(pair_id) is None:
            return pair_id


def store_discord_data(message):
    author = message.author
    guild = message.guild
    channel = message.channel
    database.store_discord_data(author.id, author.name, guild.id, channel.id)


def init_bot():
    global client
    logging.basicConfig(level=logging.INFO)
    client = MyClient()
    with open('src/secrets/discord_token.txt', 'r') as token:
        client.run(token.readline())


if __name__ == '__main__':
    init_bot()
