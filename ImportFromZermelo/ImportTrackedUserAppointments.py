import datetime
import sqlite3
import sys
from os.path import dirname, abspath
sys.path.append(abspath(dirname(dirname(__file__))))
from Classes.Appointment import Appointment
from UpdateSystem import TrackedUserManager
from ImportFromZermelo import Zermelo
from Classes import Utils

# Create a connection to the databases
appointmentConn = sqlite3.connect('./trackedUsrApp.db')
dbConn = sqlite3.connect('./database.db')
appointmentCursor = appointmentConn.cursor()
dbCursor = dbConn.cursor()

def saveAppointments(appointmentObjectList, user):
    """
    Saves a list of appointment objects into a database table for a specified user.

    Args:
        appointmentObjectList (dict): A dictionary where keys are week identifiers and values are lists of appointment objects.
        user (str): The user for whom the appointments are being saved.

    The function performs the following steps:
        1. Iterates over each week in the appointmentObjectList.
        2. Creates a table for the user if it does not already exist.
        3. Inserts or replaces each appointment object into the user's table.

    Each appointment object is expected to have a method `to_tuple()` that returns a tuple of its attributes in the correct order.
    """
    table = f""" CREATE TABLE IF NOT EXISTS '{user}' (
        id INTEGER PRIMARY KEY,
        appointmentInstance TEXT,
        start INTEGER,
        end INTEGER,
        startTimeSlot INTEGER,
        endTimeSlot INTEGER,
        branch TEXT,
        type TEXT,
        groupsInDepartments TEXT,
        locationsOfBranch TEXT,
        optional BOOLEAN,
        valid BOOLEAN,
        cancelled BOOLEAN,
        cancelledReason TEXT,
        modified BOOLEAN,
        teacherChanged BOOLEAN,
        groupChanged BOOLEAN,
        locationChanged BOOLEAN,
        timeChanged BOOLEAN,
        moved BOOLEAN,
        created INTEGER,
        hidden BOOLEAN,
        changeDescription TEXT,
        schedulerRemark TEXT,
        content TEXT,
        lastModified INTEGER,
        new BOOLEAN,
        choosableInDepartments TEXT,
        choosableInDepartmentCodes TEXT,
        extraStudentSource TEXT,
        onlineLocationUrl TEXT,
        expectedStudentCount INTEGER,
        expectedStudentCountOnline INTEGER,
        udmUUID TEXT,
        creator TEXT,
        onlineStudents TEXT,
        appointmentLastModified INTEGER,
        remark TEXT,
        availableSpace INTEGER,
        subjects TEXT,
        teachers TEXT,
        onlineTeachers TEXT
    ); """
    appointmentCursor.execute(table)
    for week in appointmentObjectList:
        for appointmentObject in appointmentObjectList[week]:
            appointmentCursor.execute(f"INSERT OR REPLACE INTO '{user}' VALUES ({', '.join(['?'] * 42)})", appointmentObject.to_tuple())

# user is the student id or teacher code
# also automatically saves
def ImportAppointments(user, startWeek, endWeek, userType : Utils.UserType, modifiedSince = None):
    # Check if the user is a brugger
    if userType == Utils.UserType.STUDENT:
        if startWeek <= 33:
            userObject = dbCursor.execute(f"SELECT departmentOfBranchCode FROM STUDENTS WHERE student = '{user}'").fetchone()
            print(userObject[0])
            if "1" in userObject[0]:
                startWeek = 34
    try:
        list_of_appointments = Zermelo.get_appointments(startWeek, endWeek, user, modifiedSince=modifiedSince)
    except Exception as e:
        if "403" in str(e) and startWeek <= 33:
            # Try again, but with week 34
            list_of_appointments = Zermelo.get_appointments(34, endWeek, user, modifiedSince=modifiedSince)
        else:
            raise e
    # sort the appointments by week
    appointmentObjectList = {}
    for appointment in list_of_appointments:
        appointmentObject = Appointment(appointment)
        # print(appointmentObject)
        week = datetime.datetime.fromtimestamp(appointmentObject.start).isocalendar()[1]
        # print("Week: ", week)
        if week in appointmentObjectList: appointmentObjectList[week].append(appointmentObject)
        else: appointmentObjectList[week] = [appointmentObject]
        # print("Type: " + str(type(appointmentObjectList[week])))
    saveAppointments(appointmentObjectList, user)
    appointmentConn.commit()
    return appointmentObjectList

def ImportAllAppointments():
    trackedUsers = TrackedUserManager.getTrackedUsers()
    appointmentList = []
    for user in trackedUsers:
        appointmentList.append(ImportAppointments(user['id'], 34, 52, Utils.UserType(user['type'])))
    appointmentList = list(filter(None, appointmentList))
    return appointmentList

def ImportAllModifiedAppointments():
    trackedUsers = TrackedUserManager.getTrackedUsers()
    appointmentList = []
    for user in trackedUsers:
        lastModified = appointmentCursor.execute(f"SELECT lastModified FROM '{user['id']}' ORDER BY lastModified DESC LIMIT 1").fetchone()
        if lastModified is not None:
            appointmentList.append(ImportAppointments(user['id'], 34, 52, Utils.UserType(user['type']), lastModified[0]))
        else:
            raise ValueError(f"User {user['id']} has no appointments")
        # appointmentList.append(ImportAppointments(user['id'], 34, 52, Utils.UserType(user['type'])))
    appointmentList = list(filter(None, appointmentList))
    return appointmentList

def ImportAppointmentsForNewUsers():
    oldUsers = appointmentCursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    trackedUsers = TrackedUserManager.getTrackedUsers()
    newUsers = [user for user in trackedUsers if user['id'] not in [oldUser[0] for oldUser in oldUsers]]
    appointmentList = []
    for user in newUsers:
        appointmentList.append(ImportAppointments(user['id'], 34, 52, Utils.UserType(user['type'])))
    appointmentList = list(filter(None, appointmentList))
    return appointmentList

def close():
    appointmentConn.close()