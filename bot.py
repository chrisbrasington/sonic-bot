#!/usr/bin/env python3
import discord
from discord.ext import commands
import configparser
from sonic_ascii import SONIC_WINK, SONIC_COFFEE

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

bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if isinstance(message.channel, discord.DMChannel) and message.author.id == authorized_user_id:
        target_channel = bot.get_channel(target_channel_id)
        if target_channel:
            if message.content.lower() == "delete" or message.content.lower() == "d":
                async for msg in target_channel.history(limit=10):
                    if msg.author == bot.user:
                        await msg.delete()
                        break
            elif message.content.lower().startswith("tag"):
                cleaned_message = message.content[3:].strip()
                await target_channel.send(f'<@{target_user_id}> {cleaned_message}')
            else:
                await target_channel.send(f'{message.content}')
        else:
            print("Target channel not found.")
    elif isinstance(message.channel, discord.TextChannel) and bot.user in message.mentions:
        await message.channel.send(f'```{SONIC_WINK}```')

bot.run(TOKEN)