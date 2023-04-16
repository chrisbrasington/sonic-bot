#!/usr/bin/env python3
import discord
from discord.ext import commands
import configparser, datetime
from sonic_ascii import SONIC_WINK, SONIC_COFFEE
import random, requests
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import openai

config = configparser.ConfigParser()
config.read('config.ini')

TOKEN = config.get('Discord', 'TOKEN')

last_sonic_coffee_sent = None
target_count = 0

bot = commands.Bot(
    command_prefix="/",
    case_insensitive=True,
    intents=discord.Intents.default())

authorized_user_id = int(config.get('UserIDs', 'AUTHORIZED_USER'))
target_user_id = int(config.get('UserIDs', 'TARGET_USER'))
target_channel_id = int(config.get('UserIDs', 'TARGET_CHANNEL'))
OPENAI_API_KEY = config.get('OpenAi', 'TOKEN')
openai.api_key = OPENAI_API_KEY

debug = False

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

MEME_API_URL = 'http://meme-api.com/gimme/sonicmemes'

sonic_positive_responses = [
    "Thanks, buddy! You're awesome too!",
    "Gotta love some good vibes!",
    "Keep spreading positivity, and we'll make this world a better place!",
    "You're a true friend! Let's collect some rings together!",
    "Hey, you're as cool as ice! And I know a thing or two about Ice Cap Zone!",
    "Together, we're unstoppable!",
    "You're as fast as the wind, and as bright as the sun!",
    "Thanks for being a part of the team!",
    "I'm all about the good vibes, and you're bringing them!",
    "Way past cool! Keep being amazing!"
]
sonic_neutral_responses = [
    "Let's talk about something fun, like collecting rings!",
    "How about we share some chili dogs?",
    "So, have you seen Tails lately?",
    "Did you know I can spin dash really fast?",
    "Let's discuss our favorite zones!",
    "Have you ever tried running at supersonic speed?",
    "Green Hill Zone sure is beautiful!",
    "I wonder what Dr. Eggman is planning this time...",
    "Chaos Emeralds are pretty powerful, don't you think?",
    "Do you have a favorite Sonic game?"
]
sonic_funny_responses = [
    "You're too slow! Can't catch up with my comebacks!",
    "You must be Dr. Eggman in disguise, trying to slow me down!",
    "Oh, you think you're tough? I've defeated Robotnik, you're nothing!",
    "No time for haters, gotta go fast!",
    "Hey, if I wanted to hear from an egghead, I'd go find Dr. Eggman!",
    "You must be one of those Badniks, always causing trouble!",
    "Too bad your attitude doesn't match your speed, or you'd be the fastest person alive!",
    "Well, at least I can outrun your negativity!",
    "I'm too busy collecting rings to care about your mean words!",
    "Why so serious? Lighten up, buddy! We've got a world to save!"
]

def generate_chatgpt_response(prompt, model="text-davinci-002", max_tokens=50):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )

    if response.choices:
        return response.choices[0].text.strip()
    else:
        return None


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
    global debug, last_sonic_coffee_sent, target_count  

    if message.author.bot:
        return

    if isinstance(message.channel, discord.DMChannel) and message.author.id == authorized_user_id:
        print(f'direct message: {message.content}')
        target_channel = bot.get_channel(target_channel_id)
        if target_channel: 
            if message.content.lower() == "debug on":
                debug = True
                await message.channel.send("Debug mode enabled.")
                print('enabling debug')
                return
            elif message.content.lower() == "debug off":
                debug = False
                await message.channel.send("Debug mode disabled.")
                print('disabling debug')
                return
            # print(message.content.lower())
            if message.content.lower().startswith("delete") or message.content.lower() == "d":
                # Extract the message ID if provided.
                message_id_to_delete = message.content[6:].strip()

                if message_id_to_delete.isdigit():
                    print(f'deleting message {message_id_to_delete}')
                    # If a message ID is provided, try to delete the message with that ID.
                    message_to_delete = await target_channel.fetch_message(int(message_id_to_delete))
                    if message_to_delete:
                        await message_to_delete.delete()
                else:
                    print('deleting prior message')
                    # If no message ID is provided, delete the last message sent by the bot.
                    async for msg in target_channel.history(limit=10):
                        if msg.author == bot.user:
                            await msg.delete()
                            break

            elif message.content.lower() == "meme" or message.content.lower() == 'm':
                print('meme response')
                meme_url = get_random_sonic_meme()
                if meme_url:
                    await target_channel.send(meme_url)
                else:
                    await target_channel.send("Failed to fetch a random Sonic meme.")
            elif message.content.lower().startswith("tag"):
                print('forwarding message with tag')
                cleaned_message = message.content[3:].strip()
                await target_channel.send(f'<@{target_user_id}> {cleaned_message}')
            else:
                print('forwarding message')
                await target_channel.send(f'{message.content}')
        else:
            print("Target channel not found.")
    elif isinstance(message.channel, discord.TextChannel):
        content_lower = message.content.lower()
        # if message.author.id == target_user_id:
        #     if last_sonic_coffee_sent is None or (datetime.datetime.now() - last_sonic_coffee_sent).days >= 1:
        #         coffee_chunks = split_string_into_chunks(SONIC_COFFEE, 1990)  # Use 1990 to leave space for the backticks.
        #         for chunk in coffee_chunks:
        #             await message.channel.send(f'```{chunk}```')
        #         last_sonic_coffee_sent = datetime.datetime.now()
        if bot.user in message.mentions:
            print('sonic-bot mentioned in channel')
            if 'meme' in content_lower or content_lower == 'm':
                print('meme response')
                meme_url = get_random_sonic_meme()
                if meme_url:
                    await message.channel.send(f'Here\'s your meme:\n{meme_url}')
                else:
                    await message.channel.send("Failed to fetch a random Sonic meme.")
            else:
                print('analyzing... ',end='')
                sentiment = sia.polarity_scores(message.content)
                print(sentiment)

                if sentiment['neg'] > sentiment['pos']:
                    print('  nevative')
                    response = random.choice(sonic_funny_responses)
                elif sentiment['pos'] > sentiment['neu']:
                    print('  positive')
                    response = random.choice(sonic_positive_responses)
                else:
                    print('  neutral')
                    response = random.choice(sonic_neutral_responses)

                if debug:
                    response = f'analysis: {sentiment}\n{response}'

                print(response)
                await message.channel.send(f'<@{message.author.id}> {response}')

                # prompt = f"Sonic says: {message.content}"
                # response = generate_chatgpt_response(prompt)

                # if response:
                #     await message.channel.send(f'<@{message.author.id}> {response}')
                # else:
                #     await message.channel.send("Oops! I couldn't generate a response.")

bot.run(TOKEN)