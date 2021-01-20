import os

from dotenv import load_dotenv
from discord.ext import commands
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CENSORED_KEYWORD = os.getenv("CENSORED_KEYWORD").split()
GUILD = os.getenv("DISCORD_GUILD")

COMMAND = '&'
ADD_REACTION = False

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or(COMMAND), intents=intents)

@bot.event
async def on_connect():
    print(f"Connected to Discord. Getting ready...")

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild: \n'
        f'{guild.name} (id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    for censorWord in CENSORED_KEYWORD:
        if censorWord in message.content:
            await message.delete()
            return
    if ADD_REACTION:
        await message.add_reaction("🐂")

    if bot.user.mentioned_in(message) and message.mention_everyone is False:
        await message.channel.send("Sup")

    await bot.process_commands(message)

@bot.command()
async def hi(ctx):
    await ctx.send('你好！')

@bot.command()
async def worldline(ctx):
    await ctx.channel.send(file=discord.File('data/steinsgate.jpg'))

def is_Labmem():
    def predicate(ctx):
        for role in ctx.message.author.roles:
            if role.name == "Labmem":
                return True
        return False
    return commands.check(predicate)

@bot.command()
@is_Labmem()
async def mention(ctx, user : discord.Member, times):
    try:
        int(times)
    except ValueError:
        return
    for _ in range(int(times)):
        await ctx.send(user.mention)

bot.run(TOKEN)