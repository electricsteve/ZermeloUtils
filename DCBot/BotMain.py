import ast
import sqlite3
import sys
import datetime
import json

from enum import Enum
from os.path import dirname, abspath

import discord
from discord import interactions, InteractionResponded
from discord.app_commands import guilds, describe, CommandTree, Group, rename
from discord.ext import tasks
from dotenv import find_dotenv, get_key

sys.path.append(abspath(dirname(dirname(__file__))))
from Classes.Student import Student
from DCBot.Embeds import AppEmbedType, appointments_embeds, default_embed, exception_embed, list_embed, error_embed
from DCBot import Embeds
from UpdateSystem import TrackedUserManager
from Classes import Utils
from ImportFromZermelo import ImportTrackedUserAppointments
from Classes.Appointment import Appointment

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Appointment):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)

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
        start = datetime.datetime.fromtimestamp(appointment[2])
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
# emojis, will be replaced
minus = get_key(dotenv_path, 'MINUS')
plus = get_key(dotenv_path, 'PLUS')
nine = get_key(dotenv_path, 'NINE')
eight = get_key(dotenv_path, 'EIGHT')
seven = get_key(dotenv_path, 'SEVEN')
six = get_key(dotenv_path, 'SIX')
five = get_key(dotenv_path, 'FIVE')
four = get_key(dotenv_path, 'FOUR')
three = get_key(dotenv_path, 'THREE')
two = get_key(dotenv_path, 'TWO')
one = get_key(dotenv_path, 'ONE')

update_channel = get_key(dotenv_path, 'UPDATE_CHANNEL')

# times for the tasks, times below are utc, but are intended for cest
trackedUsersUpdateTimes = [
    datetime.time(hour=6),
    datetime.time(hour=7),
    datetime.time(hour=8),
    datetime.time(hour=9),
    datetime.time(hour=10),
    datetime.time(hour=11),
    datetime.time(hour=12),
    datetime.time(hour=13),
    datetime.time(hour=14),
    datetime.time(hour=19),
    datetime.time(hour=21),
    datetime.time(hour=23),
]

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
# Students
@tree.command(name='students', description='Get all students', guild=discord.Object(id=test_guild))
async def studentsCommand(interaction : interactions.Interaction):
    dbCursor.execute("SELECT * FROM STUDENTS")
    studentList = dbCursor.fetchall()
    studentAmount = len(studentList)
    studentList.sort(key=lambda x: x[6])
    studentList = [(i[6]) for i in studentList]
    embed, view = list_embed("Students", f"All students\nNumber of students: {studentAmount}", studentList, interaction, fieldListLimit=50, fieldLimit=3)
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
    embed, view = list_embed("Locations", f"All locations\nNumber of locations: {locationAmount}", locationList, interaction, fieldListLimit=50, fieldTitle=True)
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
    embed, view = list_embed("Teachers", f"All teachers\nNumber of teachers: {teacherAmount}", teacherList, interaction, fieldListLimit=50)
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
    embed, view = list_embed("Groups", f"All groups\nNumber of groups: {groupAmount}", groupList, interaction, fieldListLimit=50)
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

# tracked users
@guilds(discord.Object(id=test_guild))
class TrackedUserGroup(Group):
    ...
trackedUserGroup = TrackedUserGroup(name='trackedusers', description='Tracked users system')
@trackedUserGroup.command(name='add', description='Add a tracked user')
@describe(userType='Type of user', id='Id of user')
@rename(userType='type', id='id')
async def addTrackedUserCommand(interaction : interactions.Interaction, userType : str, id : str):
    if not Utils.user_exists(id, Utils.UserType(userType.lower())):
        embed = error_embed("User not found!", f"User with id {id} and type {userType} not found", interaction)
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(embed=embed)
        return
    try:
        TrackedUserManager.addTrackedUser(userType.lower(), id)
    except ValueError:
        embed = default_embed("User already tracked!", f"User with id {id} and type {userType} is already being tracked.", 0xff6200, interaction)
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(embed=embed)
        return
    user = Utils.get_user(id, Utils.UserType(userType))
    embed = default_embed(f"<:plus:{plus}> Tracked user added!", f"{userType.capitalize()} {user.get_name()} was added as a tracked user.", 2424576, interaction)
    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(embed=embed)
@trackedUserGroup.command(name='remove', description='Remove a tracked user')
@describe(userType='Type of user', id='Id of user')
@rename(userType='type', id='id')
async def removeTrackedUserCommand(interaction : interactions.Interaction, userType : str, id : str):
    if not Utils.user_exists(id, Utils.UserType(userType.lower())):
        embed = error_embed("User not found!", f"User with id {id} and type {userType} not found", interaction)
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(embed=embed)
        return
    try :
        TrackedUserManager.removeTrackedUser(userType.lower(), id)
    except ValueError:
        embed = default_embed("User not on tracked user list!", f"User with id {id} and type {userType} is/was not being tracked.", 0xff6200, interaction)
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(embed=embed)
        return
    user = Utils.get_user(id, Utils.UserType(userType))
    embed = default_embed(f"<:minus:{minus}> Tracked user removed! ", f"{userType.capitalize()} {user.get_name()} was removed as a tracked user.", 2424576, interaction)
    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(embed=embed)
@trackedUserGroup.command(name='list', description='List all tracked users')
async def listTrackedUsersCommand(interaction : interactions.Interaction):
    trackedUsers = TrackedUserManager.getTrackedUsers()
    trackedUsers = [f"{user['type']} {user['id']}" for user in trackedUsers]
    embed, view = list_embed("Tracked users", f"All tracked users\nNumber of tracked users: {len(trackedUsers)}", trackedUsers, interaction, fieldListLimit=50)
    if view is not None:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(embed=embed, view=view)
    else:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(embed=embed)
@trackedUserGroup.command(name='update', description='Update tracked users schedules.')
async def triggerUpdateCommand(interaction : interactions.Interaction):
    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(embed=Embeds.processing_embed(interaction))
    ImportTrackedUserAppointments.ImportAppointmentsForNewUsers()
    modifiedApp = ImportTrackedUserAppointments.ImportAllModifiedAppointments()
    with open(f'./logs/TrackedUserUpdate{datetime.datetime.now().strftime("-%Y%m%d-%H%M%S%f")}.json', 'w') as f:
        # noinspection PyTypeChecker
        json.dump(modifiedApp, f, cls=CustomEncoder, indent=4)
    if len(modifiedApp) == 0:
        embed = Embeds.default_embed("No updates", "No updates found", 0xff6200, interaction)
        # noinspection PyUnresolvedReferences
        await interaction.edit_original_response(content=None, embed=embed)
        return
    channel = client.get_channel(int(update_channel))
    message = await channel.send("Update posted")
    embed = default_embed("Update posted", f"Update posted in {channel.mention} ([Message]({message.jump_url}))", 2424576, interaction)
    # noinspection PyUnresolvedReferences
    await interaction.edit_original_response(content=None, embed=embed)

# @tasks.loop(time=trackedUsersUpdateTimes)
# async def trackedUsersUpdate():
#     ImportTrackedUserAppointments.ImportAppointmentsForNewUsers()


@tree.command(name='error-test', guild=discord.Object(id=test_guild))
async def errorTest(interaction : interactions.Interaction):
    raise Exception("Test error")

@tree.error
async def on_error(interaction : interactions.Interaction, error):
    embedvar = exception_embed(error, interaction)
    # noinspection PyUnresolvedReferences
    try:
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(embed=embedvar)
    except InteractionResponded:
        await interaction.edit_original_response(content=None, embed=embedvar)

@client.event
async def on_ready():
    tree.add_command(scheduleGroup)
    tree.add_command(trackedUserGroup)
    await tree.sync(guild=discord.Object(id=test_guild))
    print(f'We have logged in as {client.user}')
# @tree.error
# async def on_error(interaction : Interaction, error : app_commands.AppCommandError):
#     print(error)
#     print(error.__traceback__.)
#     await interaction.response.send_message("An error occurred")
client.run(token)