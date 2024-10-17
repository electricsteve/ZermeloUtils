import discord.interactions
from discord import Embed, ui
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

class ListEmbedView(ui.View):
    def __init__(self, embeds : list[Embed]):
        super().__init__()
        self.embeds = [embed.set_author(name=f"Page {embeds.index(embed) + 1} out of {len(embeds)}") for embed in embeds]
        self.current = 0

    @ui.button(label="Previous", style=discord.ButtonStyle.blurple, disabled=True)
    async def prev(self, interaction, button):
        if self.current > 0:
            self.current -= 1
            self.children[1].disabled = False
            if self.current == 0:
                button.disabled = True
            await interaction.response.edit_message(embed=self.embeds[self.current], view=self)

    @ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def next(self, interaction, button):
        if self.current < len(self.embeds) - 1:
            self.current += 1
            self.children[0].disabled = False
            if self.current == len(self.embeds) - 1:
                button.disabled = True
            await interaction.response.edit_message(embed=self.embeds[self.current], view=self)

def default_embed(title, description, color, interaction):
    embedVar = Embed(title=title, description=description, color=color, timestamp=interaction.created_at)
    embedVar.set_footer(text=f"ZermeloUtils ({school})")
    return embedVar

def list_embed(title, description, textList, interaction, fieldListLimit=1024, fieldTitle=False, fieldLimit=25):
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
    for i in range(len(textList)):
        FieldCharLen += len(textList[i]) + 2
        EmbedCharLen += len(textList[i]) + 2
        if EmbedCharLen >= 6000:
            embedVar.add_field(name=get_field_title(), value=Field, inline=True)
            embeds.append(embedVar)
            embedVar = default_embed(title, description, 2424576, interaction)
            EmbedCharLen = len(embedVar.description) + len(embedVar.title) + len(embedVar.footer.text)
            FieldCharLen = len(textList[i])
            Field = textList[i]
        else:
            if FieldCharLen >= 1024 or len(Field.split("\n")) >= fieldListLimit:
                embedVar.add_field(name=get_field_title(), value=Field, inline=True)
                if len(embedVar.fields) >= fieldLimit:
                    embeds.append(embedVar)
                    embedVar = default_embed(title, description, 2424576, interaction)
                    EmbedCharLen = len(embedVar.description) + len(embedVar.title) + len(embedVar.footer.text)
                FieldCharLen = len(textList[i])
                Field = textList[i]
            elif Field == "":
                Field = textList[i]
            else:
                Field += "\n" + textList[i]
    embedVar.add_field(name=get_field_title(), value=Field, inline=True)
    embeds.append(embedVar)
    if len(embeds) > 1:
        return embeds[0], ListEmbedView(embeds)
    return embeds[0], None

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