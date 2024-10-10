from discord import Embed
from dotenv import find_dotenv, get_key
from enum import Enum
from ast import literal_eval
import sqlite3

dotenv_path = find_dotenv()
school = get_key(dotenv_path, 'SCHOOL')

dbConn = sqlite3.connect("./database.db")
dbCursor = dbConn.cursor()

locations = {}
groups = {}

class AppEmbedType(Enum):
    TEACHER = 1
    STUDENT = 2
    LOCATION = 3

def default_embed(title, description, color, interaction):
    embedVar = Embed(title=title, description=description, color=color, timestamp=interaction.created_at)
    embedVar.set_footer(text=f"ZermeloUtils ({school})")
    return embedVar

def error_embed(error, interaction):
    title = "Error"
    description = f"An error occurred: {error}"
    return default_embed(title, description, 0xff0000, interaction)

# Embed for appointments for week
def appointments_embed(object, appointments, week, appEmbedType : AppEmbedType, interaction):
    var1 = ""
    if appEmbedType == AppEmbedType.TEACHER:
        var1 = f"{object[7]} ({object[1]})"
    elif appEmbedType == AppEmbedType.STUDENT:
        var1 = f"{object[6]} ({object[1]})"
    elif appEmbedType == AppEmbedType.LOCATION:
        var1 = f"{object[1]}"
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