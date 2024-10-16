import discord.interactions
from discord import Embed
from dotenv import find_dotenv, get_key
from enum import Enum
from ast import literal_eval
import sqlite3
import traceback
import os

dotenv_path = find_dotenv()
school = get_key(dotenv_path, 'SCHOOL')

dbConn = sqlite3.connect("./database.db")
dbCursor = dbConn.cursor()

locations = {}
groups = {}

if not os.path.isdir("./logs"):
    os.makedirs("./logs")
if not os.path.isdir("./logs/errors"):
    os.makedirs("./logs/errors")

class AppEmbedType(Enum):
    TEACHER = 1
    STUDENT = 2
    LOCATION = 3

def default_embed(title, description, color, interaction):
    embedVar = Embed(title=title, description=description, color=color, timestamp=interaction.created_at)
    embedVar.set_footer(text=f"ZermeloUtils ({school})")
    return embedVar

def list_embed(title, description, list, interaction, listLimit=1024, fieldTitle=False):
    def get_field_title():
        if fieldTitle:
            return f"{i + 1 - len(Field.split('\n'))} - {i + 1}"
        else:
            return f""
    embeds = []
    embedVar = default_embed(title, description, 2424576, interaction)
    EmbedCharLen = len(embedVar.description) + len(embedVar.title) + len(embedVar.footer.text)
    FieldCharLen = 0
    Field = ""
    for i in range(len(list)):
        FieldCharLen += len(list[i]) + 2
        EmbedCharLen += len(list[i]) + 2
        if EmbedCharLen >= 6000:
            print(EmbedCharLen)
            print(FieldCharLen)
            print("Too long")
            embedVar.add_field(name=get_field_title(), value=Field, inline=True)
            embeds.append(embedVar)
            embedVar = default_embed(title, description, 2424576, interaction)
            EmbedCharLen = len(embedVar.description) + len(embedVar.title) + len(embedVar.footer.text)
            FieldCharLen = len(list[i])
            Field = list[i]
        else:
            if FieldCharLen >= 1024 or len(Field.split("\n")) >= listLimit:
                embedVar.add_field(name=get_field_title(), value=Field, inline=True)
                FieldCharLen = len(list[i])
                Field = list[i]
            elif Field == "":
                Field = list[i]
            else:
                Field += "\n" + list[i]
    embedVar.add_field(name=get_field_title(), value=Field, inline=True)
    embeds.append(embedVar)
    return embeds

def error_embed(error, interaction : discord.interactions.Interaction):
    st = traceback.format_exc()
    fileName = f"./logs/errors/error{interaction.created_at.strftime('-%Y_%m_%d-%H_%M_%S')}.log"
    with open(fileName, "w") as f:
        f.write(st)
    title = "Error"
    description = f"An error occurred: {error}\nFull stack trace saved to file: {fileName}."
    return default_embed(title, description, 0xff0000, interaction)

# Embed for appointments for week
def appointments_embed(obj, appointments, week, appEmbedType : AppEmbedType, interaction):
    var1 = ""
    if appEmbedType == AppEmbedType.TEACHER:
        var1 = f"{obj[7]} ({obj[1]})"
    elif appEmbedType == AppEmbedType.STUDENT:
        var1 = f"{obj[6]} ({obj[1]})"
    elif appEmbedType == AppEmbedType.LOCATION:
        var1 = f"{obj[1]}"
    embedVar = default_embed("Schedule", f"Schedule for {var1} for week {week}", 2424576, interaction)
    for day in appointments:
        value = ""
        for appointment in appointments[day]:
            timeslot = appointment[4]
            subjects = literal_eval(appointment[39])
            teachers = literal_eval(appointment[40])
            groupsApp = literal_eval(appointment[8])
            locationsApp = literal_eval(appointment[9])
            for i in range(len(locationsApp)):
                loc = locationsApp[i]
                if loc not in locations:
                    locations[loc] = dbCursor.execute("SELECT * FROM LOCATIONS WHERE id = ?", (loc,)).fetchone()[1]
                locationsApp[i] = locations[loc]
            for i in range(len(groupsApp)):
                group = groupsApp[i]
                if group not in groups:
                    groups[group] = dbCursor.execute("SELECT * FROM GROUPS WHERE id = ?", (group,)).fetchone()[5]
                groupsApp[i] = groups[group]
            if appointment[12] == 1: # Cancelled
                if appEmbedType == AppEmbedType.TEACHER:
                    value += f"- :no_entry: :number_{timeslot}: ~~{', '.join(subjects)} - {', '.join(groupsApp)} - {', '.join(locationsApp)}~~\n"
                elif appEmbedType == AppEmbedType.STUDENT:
                    value += f"- :no_entry: :number_{timeslot}: ~~{', '.join(subjects)} - {', '.join(teachers)} - {', '.join(locationsApp)}~~\n"
                elif appEmbedType == AppEmbedType.LOCATION:
                    value += f"- :no_entry: :number_{timeslot}: ~~{', '.join(subjects)} - {', '.join(teachers)} - {', '.join(groupsApp)}~~\n"
            else:
                if appEmbedType == AppEmbedType.TEACHER:
                    value += f"- :number_{timeslot}: {', '.join(subjects)} - {', '.join(groupsApp)} - {', '.join(locationsApp)}\n"
                elif appEmbedType == AppEmbedType.STUDENT:
                    value += f"- :number_{timeslot}: {', '.join(subjects)} - {', '.join(teachers)} - {', '.join(locationsApp)}\n"
                elif appEmbedType == AppEmbedType.LOCATION:
                    value += f"- :number_{timeslot}: {', '.join(subjects)} - {', '.join(teachers)} - {', '.join(groupsApp)}\n"
        embedVar.add_field(name=f"{day}", value=value, inline=True)
    return embedVar

# Multiple embeds for appointments for multiple weeks
def appointments_embeds(object, appointments, type : AppEmbedType, interaction):
    embeds = []
    for week in appointments:
        embeds.append(appointments_embed(object, appointments[week], week, type, interaction))
    return embeds