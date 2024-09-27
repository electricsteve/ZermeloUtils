import discord
from discord import app_commands, interactions
from dotenv import find_dotenv, get_key
import sqlite3
import os
import sys
from os.path import dirname, abspath
sys.path.append(abspath(dirname(dirname(__file__))))
from Classes.Student import Student

def in_common(student1, student2):
    studentObject1 = Student.from_tuple(student1)
    studentObject2 = Student.from_tuple(student2)
    return studentObject1.in_common(studentObject2, conn)

dotenv_path = find_dotenv()
token = get_key(dotenv_path, 'DISCORD_TOKEN')
test_guild = get_key(dotenv_path, 'TEST_GUILD')
school = get_key(dotenv_path, 'SCHOOL')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)

conn = sqlite3.connect('./database.db')
c = conn.cursor()

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=test_guild))
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

@tree.command(name='ping', description='Get bot ping', guild=discord.Object(id=test_guild))
async def ping(interaction):
    await interaction.response.send_message(f'PONG! Latency: {int(str(client.latency) * 1000)}ms')
@tree.command(name='locations', description='Get all locations', guild=discord.Object(id=test_guild))
async def locations(interaction : interactions.Interaction):
    c.execute("SELECT * FROM LOCATIONS")
    locationList = c.fetchall()
    locationList.sort(key=lambda x: x[1])
    locationList = [(i[1]) for i in locationList]
    embedvar = discord.Embed(title="Locations", description=f"All locations (classrooms, gym, etc.) from {school}", color=2424576, timestamp=interaction.created_at)
    embedvar.description += f"\n\nNumber of locations: {len(locationList)}"
    embedvar.set_footer(text="ZermeloUtils")
    for location in locationList:
        embedvar.description += f"\n- {location}"
    await interaction.response.send_message(embed=embedvar)
@tree.command(name='incommon', description='Get lessons and groups 2 people have in common', guild=discord.Object(id=test_guild))
@app_commands.describe(student1='First student', student2='Second student')
async def incommon(interaction : interactions.Interaction, student1 : str, student2 : str):
    c.execute("SELECT * FROM STUDENTS WHERE student = ? OR student = ?", (student1, student2))
    students = c.fetchall()
    if len(students) < 2:
        await interaction.response.send_message("One of the students is not in the database")
        return
    common = in_common(students[0], students[1])
    embedvar = discord.Embed(title="In Common", description=f"Groups in common between {students[0][6]} ({students[0][1]}) and {students[1][6]} ({students[1][1]})", color=2424576, timestamp=interaction.created_at)
    embedvar.description += f"\n\nNumber of groups in common: {len(common)}"
    for group in common:
        embedvar.description += f"\n- {group}"
    embedvar.set_footer(text="ZermeloUtils")
    await interaction.response.send_message(embed=embedvar)

client.run(token)