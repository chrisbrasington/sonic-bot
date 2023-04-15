import discord
from discord.ext import commands
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

TOKEN = config.get('Discord', 'TOKEN')

intents = discord.Intents.default()
intents.direct_messages = True
intents.guild_messages = False
bot = commands.Bot(command_prefix='!', intents=intents)

authorized_user_id = int(config.get('UserIDs', 'AUTHORIZED_USER'))
target_channel_id = int(config.get('UserIDs', 'TARGET_CHANNEL'))
target_user_id = int(config.get('UserIDs', 'TARGET_USER'))

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
            await target_channel.send(f'<@{target_user_id}> {message.content}')
        else:
            print("Target channel not found.")

bot.run(TOKEN)
