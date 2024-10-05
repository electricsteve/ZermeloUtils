import ast
import sqlite3
import sys
from datetime import datetime
from enum import Enum
from os.path import dirname, abspath

import discord
from discord import interactions
from discord.app_commands import guilds, describe, CommandTree, Group, rename
from dotenv import find_dotenv, get_key

sys.path.append(abspath(dirname(dirname(__file__))))
from Classes.Student import Student

class WeekDay(Enum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6

def in_common(student1, student2):
    studentObject1 = Student.from_tuple(student1)
    studentObject2 = Student.from_tuple(student2)
    return studentObject1.in_common(studentObject2, dbConn)

def sort_appointments(appointmentsInput):
    appointmentsOutput = {}
    appointmentsInput.sort(key=lambda x: x[2])
    for appointment in appointmentsInput:
        start = datetime.fromtimestamp(appointment[2])
        week = start.isocalendar()[1]
        day = WeekDay(start.weekday()).name
        if week not in appointmentsOutput:
            appointmentsOutput[week] = {}
        if day not in appointmentsOutput[week]:
            appointmentsOutput[week][day] = []
        appointmentsOutput[week][day].append(appointment)
    return appointmentsOutput

def check_if_week_exists(week : int):
    appointmentsCursor.execute(f"SELECT * FROM sqlite_master WHERE type='table' AND name={week}")
    week = appointmentsCursor.fetchone()
    return week is not None

dotenv_path = find_dotenv()
token = get_key(dotenv_path, 'DISCORD_TOKEN')
test_guild = get_key(dotenv_path, 'TEST_GUILD')
school = get_key(dotenv_path, 'SCHOOL')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = CommandTree(client)
dbConn = sqlite3.connect('./database.db')
dbCursor = dbConn.cursor()
appointmentsConn = sqlite3.connect('./appointments.db')
appointmentsCursor = appointmentsConn.cursor()

# ping
@tree.command(name='ping', description='Get bot ping', guild=discord.Object(id=test_guild))
async def ping(interaction):
    await interaction.response.send_message(f'PONG! Latency: {str(int(client.latency * 1000))}ms')
# locations
@tree.command(name='locations', description='Get all locations', guild=discord.Object(id=test_guild))
async def locationsCommand(interaction : interactions.Interaction):
    dbCursor.execute("SELECT * FROM LOCATIONS")
    locationList = dbCursor.fetchall()
    locationList.sort(key=lambda x: x[1])
    locationList = [(i[1]) for i in locationList]
    embedvar = discord.Embed(title="Locations", description=f"All locations (classrooms, gym, etc.)", color=2424576, timestamp=interaction.created_at)
    embedvar.description += f"\n\nNumber of locations: {len(locationList)}"
    embedvar.set_footer(text=f"ZermeloUtils ({school})")
    for location in locationList:
        embedvar.description += f"\n- {location}"
    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(embed=embedvar)
# incommon
@tree.command(name='incommon', description='Get lessons and groups 2 people have in common', guild=discord.Object(id=test_guild))
@describe(student1='First student', student2='Second student')
async def incommonCommand(interaction : interactions.Interaction, student1 : str, student2 : str):
    if student1 == student2:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message("Please provide two different students")
        return
    dbCursor.execute("SELECT * FROM STUDENTS WHERE student = ? OR student = ?", (student1, student2))
    students = dbCursor.fetchall()
    if len(students) < 2:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message("One of the students is not in the database")
        return
    common = in_common(students[0], students[1])
    embedvar = discord.Embed(title="In Common", description=f"Groups in common between {students[0][6]} ({students[0][1]}) and {students[1][6]} ({students[1][1]})", color=2424576, timestamp=interaction.created_at)
    embedvar.description += f"\nNumber of groups in common: {len(common)}"
    for group in common:
        embedvar.description += f"\n- {group}"
    embedvar.set_footer(text=f"ZermeloUtils ({school})")
    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(embed=embedvar)
# Search
@tree.command(name='search', description='Search for student, (teacher or location later)', guild=discord.Object(id=test_guild))
@describe(searchInput='Search input')
@rename(searchInput='input')
async def searchCommand(interaction : interactions.Interaction, searchInput : str):
    dbCursor.execute("SELECT * FROM STUDENTS WHERE fullName LIKE ?", (f'%{searchInput}%',))
    students = dbCursor.fetchall()
    if len(students) == 0:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message("No students found")
        return
    embedvar = discord.Embed(title="Search", description=f"Search results for '{searchInput}'", color=2424576, timestamp=interaction.created_at)
    embedvar.description += f"\nNumber of students found: {len(students)}"
    for student in students:
        embedvar.description += f"\n- {student[6]} ({student[1]})"
    embedvar.set_footer(text=f"ZermeloUtils ({school})")
    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(embed=embedvar)
# schedules
@guilds(discord.Object(id=test_guild))
class ScheduleGroup(Group):
    ...
scheduleGroup = ScheduleGroup(name='schedule', description='Get schedule for student, teacher or location')
# student
@scheduleGroup.command(name='student', description='Get schedule for student')
@describe(studentId='Student id', week='Week number', extraWeeks='Extra weeks')
@rename(studentId='student', week='week', extraWeeks='extraweeks')
async def studentScheduleCommand(interaction : interactions.Interaction, studentId : str, week : int, extraWeeks : int = 0):
    dbCursor.execute("SELECT * FROM STUDENTS WHERE student = ?", (studentId,))
    student = dbCursor.fetchone()
    if student is None:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message("Student not found")
        return
    groupInDepartments = ast.literal_eval(student[5])
    appointments = []
    weekErrors = []
    for week in range(week, week + extraWeeks + 1):
        if not check_if_week_exists(week):
            weekErrors.append(str(week))
            continue
        for group in groupInDepartments:
            appointmentsCursor.execute(f"SELECT * FROM '{week}' WHERE groupsInDepartments LIKE '%{group}%' AND valid = 1")
            appointments += appointmentsCursor.fetchall()
    if len(weekErrors) != 0:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(f"Error: Week(s) {', '.join(weekErrors)} do(es) not exist.")
        return
    if len(appointments) == 0:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message("No appointments found.")
    appointmentsSorted = sort_appointments(appointments)
    embeds = []
    locations = {}
    for week in appointmentsSorted:
        embedvar = discord.Embed(title="Schedule", description=f"Schedule for {student[6]} ({student[1]}) for week {week}", color=2424576, timestamp=interaction.created_at)
        for day in appointmentsSorted[week]:
            value = ""
            for appointment in appointmentsSorted[week][day]:
                timeslot = appointment[4]
                subject = ast.literal_eval(appointment[39])[0]
                teacher = ast.literal_eval(appointment[40])[0]
                location = ast.literal_eval(appointment[9])[0]
                if location not in locations:
                    locations[location] = dbCursor.execute("SELECT * FROM LOCATIONS WHERE id = ?", (location,)).fetchone()[1]
                location = locations[location]
                if appointment[12] == 1: # Cancelled
                    value += f"- :no_entry: :number_{timeslot}: ~~{subject} - {teacher} - {location}~~\n"
                else:
                    value += f"- :number_{timeslot}: {subject} - {teacher} - {location}\n"
            embedvar.add_field(name=f"{day}", value=value, inline=True)
        embedvar.set_footer(text=f"ZermeloUtils ({school})")
        embeds.append(embedvar)
    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(embeds=embeds)
@scheduleGroup.command(name='teacher', description='Get schedule for teacher')
@describe(teacherId='Teacher id', week='Week number', extraWeeks='Extra weeks')
@rename(teacherId='teacher', week='week', extraWeeks='extraweeks')
async def teacherScheduleCommand(interaction : interactions.Interaction, teacherId : str, week : int, extraWeeks : int = 0):
    dbCursor.execute("SELECT * FROM TEACHERS WHERE employee = ?", (teacherId,))
    teacher = dbCursor.fetchone()
    if teacher is None:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message("Teacher not found")
        return
    appointments = []
    weekErrors = []
    for week in range(week, week + extraWeeks + 1):
        if not check_if_week_exists(week):
            weekErrors.append(str(week))
            continue
        appointmentsCursor.execute(f"SELECT * FROM '{week}' WHERE teachers LIKE '%{teacherId}%' AND valid = 1")
        appointments += appointmentsCursor.fetchall()
    if len(weekErrors) != 0:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(f"Error: Week(s) {', '.join(weekErrors)} do(es) not exist.")
        return
    if len(appointments) == 0:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message("No appointments found.")
    appointmentsSorted = sort_appointments(appointments)
    embeds = []
    locations = {}
    for week in appointmentsSorted:
        embedvar = discord.Embed(title="Schedule", description=f"Schedule for {teacher[7]} ({teacher[1]}) for week {week}", color=2424576, timestamp=interaction.created_at)
        for day in appointmentsSorted[week]:
            value = ""
            for appointment in appointmentsSorted[week][day]:
                timeslot = appointment[4]
                subject = ast.literal_eval(appointment[39])[0]
                groups = ast.literal_eval(appointment[8])
                location = ast.literal_eval(appointment[9])[0]
                if location not in locations:
                    locations[location] = dbCursor.execute("SELECT * FROM LOCATIONS WHERE id = ?", (location,)).fetchone()[1]
                location = locations[location]
                groupNames = []
                for group in groups:
                    dbCursor.execute("SELECT * FROM GROUPS WHERE id = ?", (group,))
                    groupName = dbCursor.fetchone()[5]
                    groupNames.append(groupName)
                if appointment[12] == 1: # Cancelled
                    value += f"- :no_entry: :number_{timeslot}: ~~{subject} - {', '.join(groupNames)} - {location}~~\n"
                else:
                    value += f"- :number_{timeslot}: {subject} - {', '.join(groupNames)} - {location}\n"
            embedvar.add_field(name=f"{day}", value=value, inline=True)
        embedvar.set_footer(text=f"ZermeloUtils ({school})")
        embeds.append(embedvar)
    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(embeds=embeds)

@client.event
async def on_ready():
    tree.add_command(scheduleGroup)
    await tree.sync(guild=discord.Object(id=test_guild))
    print(f'We have logged in as {client.user}')
# @tree.error
# async def on_error(interaction : Interaction, error : app_commands.AppCommandError):
#     print(error)
#     print(error.__traceback__.)
#     await interaction.response.send_message("An error occurred")
client.run(token)