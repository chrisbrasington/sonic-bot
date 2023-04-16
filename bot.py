#!/usr/bin/env python3
import discord
from discord.ext import commands
import configparser
from sonic_ascii import SONIC_WINK, SONIC_COFFEE
import requests

config = configparser.ConfigParser()
config.read('config.ini')

TOKEN = config.get('Discord', 'TOKEN')

bot = commands.Bot(
    command_prefix="/",
    case_insensitive=True,
    intents=discord.Intents.default())

authorized_user_id = int(config.get('UserIDs', 'AUTHORIZED_USER'))
target_channel_id = int(config.get('UserIDs', 'TARGET_CHANNEL'))
target_user_id = int(config.get('UserIDs', 'TARGET_USER'))

MEME_API_URL = 'http://meme-api.com/gimme/sonicmemes'

def get_random_sonic_meme():
    try:
        response = requests.get(MEME_API_URL)
        if response.status_code == 200:
            data = response.json()
            return data['url']
    except Exception as e:
        print(f'Error fetching meme: {e}')
        return None

def split_string_into_chunks(string, chunk_size):
    return [string[i:i + chunk_size] for i in range(0, len(string), chunk_size)]

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if isinstance(message.channel, discord.DMChannel) and message.author.id == authorized_user_id:
        target_channel = bot.get_channel(target_channel_id)
        if target_channel:
            # print(message.content.lower())
            if message.content.lower().startswith("delete") or message.content.lower() == "d":
                # Extract the message ID if provided.
                message_id_to_delete = message.content[6:].strip()

                if message_id_to_delete.isdigit():
                    # If a message ID is provided, try to delete the message with that ID.
                    message_to_delete = await target_channel.fetch_message(int(message_id_to_delete))
                    if message_to_delete:
                        await message_to_delete.delete()
                else:
                    # If no message ID is provided, delete the last message sent by the bot.
                    async for msg in target_channel.history(limit=10):
                        if msg.author == bot.user:
                            await msg.delete()
                            break
            elif message.content.lower().startswith("tag"):
                cleaned_message = message.content[3:].strip()
                await target_channel.send(f'<@{target_user_id}> {cleaned_message}')
            elif message.content.lower() == "meme" or message.content.lower() == 'm':
                meme_url = get_random_sonic_meme()
                if meme_url:
                    await target_channel.send(meme_url)
                else:
                    await target_channel.send("Failed to fetch a random Sonic meme.")
            else:
                await target_channel.send(f'{message.content}')
        else:
            print("Target channel not found.")
    elif isinstance(message.channel, discord.TextChannel):
        content_lower = message.content.lower()
        if bot.user in message.mentions:
            if any(greeting in content_lower for greeting in ['hi', 'hello', 'hey']):
                await message.channel.send(f'Hi, <@{message.author.id}>! Let\'s play sonic today!')
            elif 'love' or 'hate' in content_lower:
                await message.channel.send(f'I love you too <@{message.author.id}>!')
            elif 'meme' in content_lower or content_lower == 'm':
                meme_url = get_random_sonic_meme()
                if meme_url:
                    await message.channel.send(f'Here\'s your meme:\n{meme_url}')
                else:
                    await message.channel.send("Failed to fetch a random Sonic meme.")
            if message.author.id == target_user_id:
                coffee_chunks = split_string_into_chunks(SONIC_COFFEE, 1990)  # Use 1990 to leave space for the backticks.
                for chunk in coffee_chunks:
                    await message.channel.send(f'```{chunk}```')


bot.run(TOKEN)