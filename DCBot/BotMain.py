import discord
from discord import app_commands
from dotenv import find_dotenv, get_key
import sqlite3

dotenv_path = find_dotenv()
token = get_key(dotenv_path, 'DISCORD_TOKEN')
test_guild = get_key(dotenv_path, 'TEST_GUILD')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

@tree.command(name='locations', description='List all locations', guild=discord.Object(id=test_guild))
async def locations(ctx):

    await ctx.send('WIP')

client.run(token)