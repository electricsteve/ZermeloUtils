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
from DCBot.Embeds import AppEmbedType, appointments_embed, appointments_embeds, default_embed, error_embed, list_embed

class WeekDay(Enum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6

def splitList(inputList, n):
    for i in range(0, len(inputList), n):
        yield inputList[i:i + n]

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
# Students (ah HELL NAH)
@tree.command(name='students', description='Get all students', guild=discord.Object(id=test_guild))
async def studentsCommand(interaction : interactions.Interaction):
    dbCursor.execute("SELECT * FROM STUDENTS")
    studentList = dbCursor.fetchall()
    studentAmount = len(studentList)
    studentList.sort(key=lambda x: x[6])
    studentList = [(i[6]) for i in studentList]
    embed, view = list_embed("Students", f"All students\nNumber of students: {studentAmount}", studentList, interaction, listLimit=50)
    if view is not None:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(embed=embed, view=view)
    else:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(embeds=embeds)
# locations
@tree.command(name='locations', description='Get all locations', guild=discord.Object(id=test_guild))
async def locationsCommand(interaction : interactions.Interaction):
    dbCursor.execute("SELECT * FROM LOCATIONS")
    locationList = dbCursor.fetchall()
    locationAmount = len(locationList)
    locationList.sort(key=lambda x: x[1])
    locationList = [(i[1]) for i in locationList]
    embed, view = list_embed("Locations", f"All locations\nNumber of locations: {locationAmount}", locationList, interaction, listLimit=50, fieldTitle=True)
    if view is not None:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(embed=embed, view=view)
    else:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(embed=embed)
# Teachers
@tree.command(name='teachers', description='Get all teachers', guild=discord.Object(id=test_guild))
async def teachersCommand(interaction : interactions.Interaction):
    dbCursor.execute("SELECT * FROM TEACHERS")
    teacherList = dbCursor.fetchall()
    teacherAmount = len(teacherList)
    for i in range(len(teacherList)):
        if teacherList[i][7] is None:
            teacherList[i] = list(teacherList[i])
            teacherList[i][7] = teacherList[i][1]
            teacherList[i] = tuple(teacherList[i])
    teacherList.sort(key=lambda x: x[7])
    def getStr(teacher):
        name = teacher[7]
        if teacher[12] is not None:
            name += f", {teacher[12]}"
        if teacher[1] is not None:
            name += f" ({teacher[1]})"
        return name
    teacherList = [getStr(i) for i in teacherList]
    embed, view = list_embed("Teachers", f"All teachers\nNumber of teachers: {teacherAmount}", teacherList, interaction, listLimit=50)
    if view is not None:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(embed=embed, view=view)
    else:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(embed=embed)
# Groups
@tree.command(name='groups', description='Get all groups', guild=discord.Object(id=test_guild))
async def groupsCommand(interaction : interactions.Interaction):
    dbCursor.execute("SELECT * FROM GROUPS")
    groupList = dbCursor.fetchall()
    groupAmount = len(groupList)
    groupList.sort(key=lambda x: x[5])
    groupList = [(i[5]) for i in groupList]
    groupList = [', '.join(x) for x in zip(groupList[::2], groupList[1::2])]
    embed, view = list_embed("Groups", f"All groups\nNumber of groups: {groupAmount}", groupList, interaction, listLimit=50)
    if view is not None:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(embed=embed, view=view)
    else:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(embed=embed)
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
    embedvar = default_embed("In common", f"Lessons and groups {students[0][6]} and {students[1][6]} have in common", 2424576, interaction)
    embedvar.description += f"\nNumber of groups in common: {len(common)}"
    for group in common:
        embedvar.description += f"\n- {group}"
    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(embed=embedvar)
# Search
@tree.command(name='search', description='Search for students, teachers or locations', guild=discord.Object(id=test_guild))
@describe(searchInput='Search input')
@rename(searchInput='input')
async def searchCommand(interaction : interactions.Interaction, searchInput : str):
    dbCursor.execute("SELECT * FROM STUDENTS WHERE fullName LIKE ?", (f'%{searchInput}%',))
    students = dbCursor.fetchall()
    dbCursor.execute("SELECT * FROM TEACHERS WHERE lastName LIKE ? OR employee LIKE ?", (f'%{searchInput}%',f"%{searchInput}%"))
    teachers = dbCursor.fetchall()
    dbCursor.execute("SELECT * FROM LOCATIONS WHERE name LIKE ?", (f'%{searchInput}%',))
    locations = dbCursor.fetchall()
    if len(students) == 0 and len(teachers) == 0 and len(locations) == 0:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message("No results found")
        return
    embedvar = default_embed("Search", f"Search results for '{searchInput}'", 2424576, interaction)
    embedvar.description += f"\nNumber of students found: {len(students)}"
    for student in students:
        embedvar.description += f"\n- {student[6]} ({student[1]})"
    embedvar.description += f"\nNumber of teachers found: {len(teachers)}"
    for teacher in teachers:
        embedvar.description += f"\n- {teacher[7]} ({teacher[1]})"
    embedvar.description += f"\nNumber of locations found: {len(locations)}"
    for location in locations:
        embedvar.description += f"\n- {location[1]}"
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
    embeds = appointments_embeds(student, appointmentsSorted, AppEmbedType.STUDENT, interaction)
    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(embeds=embeds)
# teacher
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
    embeds = appointments_embeds(teacher, appointmentsSorted, AppEmbedType.TEACHER, interaction)
    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(embeds=embeds)
# location
@scheduleGroup.command(name='location', description='Get schedule for location')
@describe(location='Location', week='Week number', extraWeeks='Extra weeks')
@rename(location='location', week='week', extraWeeks='extraweeks')
async def locationScheduleCommand(interaction : interactions.Interaction, location : str, week : int, extraWeeks : int = 0):
    dbCursor.execute("SELECT * FROM LOCATIONS WHERE name = ?", (location,))
    location = dbCursor.fetchone()
    if location is None:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message("Location not found")
        return
    appointments = []
    weekErrors = []
    for week in range(week, week + extraWeeks + 1):
        if not check_if_week_exists(week):
            weekErrors.append(str(week))
            continue
        appointmentsCursor.execute(f"SELECT * FROM '{week}' WHERE locationsOfBranch LIKE '%{location[0]}%' AND valid = 1")
        appointments += appointmentsCursor.fetchall()
    if len(weekErrors) != 0:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(f"Error: Week(s) {', '.join(weekErrors)} do(es) not exist.")
        return
    if len(appointments) == 0:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message("No appointments found.")
    appointmentsSorted = sort_appointments(appointments)
    embeds = appointments_embeds(location, appointmentsSorted, AppEmbedType.LOCATION, interaction)
    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(embeds=embeds)

@tree.command(name='error-test', guild=discord.Object(id=test_guild))
async def errorTest(interaction : interactions.Interaction):
    raise Exception("Test error")

@tree.error
async def on_error(interaction, error):
    embedvar = error_embed(error, interaction)
    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(embed=embedvar)

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