import datetime
import sqlite3
import sys
from os.path import dirname, abspath
sys.path.append(abspath(dirname(dirname(__file__))))
from Classes.Appointment import Appointment
import Zermelo
import threading

# Create a connection to the database
appointmentConn = sqlite3.connect('./appointments.db', check_same_thread=False)
dbConn = sqlite3.connect('./database.db')
appointmentCursor = appointmentConn.cursor()
dbCursor = dbConn.cursor()

mass = False

massUsers = {}

lock = threading.Lock()

def setMass(value):
    global mass
    mass = value
    if value:
        global massUsers
        users = dbCursor.execute("SELECT student, departmentOfBranchCode FROM STUDENTS").fetchall()
        for user in users:
            if "1" in user[1]:
                massUsers[user[0]] = True
            else:
                massUsers[user[0]] = False

def saveAppointments(appointmentObjectList):
    for week in appointmentObjectList:
        table = f""" CREATE TABLE IF NOT EXISTS '{week}' (
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
        # print("Table created for week: ", week)
        # print(appointmentObjectList[week])
        # print(type(appointmentObjectList[week]))
        # print(len(appointmentObjectList[week]))
        for appointmentObject in appointmentObjectList[week]:
            appointmentCursor.execute(f"INSERT OR REPLACE INTO '{week}' VALUES ({', '.join(['?'] * 42)})", appointmentObject.to_tuple())

massAppointmentObjectList = {}

def ImportAppointments(user, startWeek, endWeek, lastModified : int = None):
    if startWeek <= 33:
        if not mass:
            userObject = dbCursor.execute(f"SELECT departmentOfBranchCode FROM STUDENTS WHERE student = {user}").fetchone()
            print(userObject[0])
            if "1" in userObject[0]:
                startWeek = 34
        else:
            if massUsers[user]:
                startWeek = 34
    try:
        list_of_appointments = Zermelo.get_appointments(startWeek, endWeek, user, modifiedSince=lastModified)
    except Exception as e:
        if "403" in str(e):
            # Try again, but with week 34
            list_of_appointments = Zermelo.get_appointments(34, endWeek, user, modifiedSince=lastModified)
        else:
            raise e
    print("Number of appointments: ", len(list_of_appointments))
    # Tables will now be per week, no longer per user
    # First, sort the appointments by week
    if not mass:
        appointmentObjectList = {}
        for appointment in list_of_appointments:
            appointmentObject = Appointment(appointment)
            # print(appointmentObject)
            week = datetime.datetime.fromtimestamp(appointmentObject.start).isocalendar()[1]
            # print("Week: ", week)
            if week in appointmentObjectList: appointmentObjectList[week].append(appointmentObject)
            else: appointmentObjectList[week] = [appointmentObject]
            # print("Type: " + str(type(appointmentObjectList[week])))
        saveAppointments(appointmentObjectList)
        appointmentConn.commit()
    else:
        with lock:
            global massAppointmentObjectList
            for appointment in list_of_appointments:
                appointmentObject = Appointment(appointment)
                # print(appointmentObject)
                week = datetime.datetime.fromtimestamp(appointmentObject.start).isocalendar()[1]
                # print("Week: ", week)
                if week in massAppointmentObjectList: massAppointmentObjectList[week].append(appointmentObject)
                else: massAppointmentObjectList[week] = [appointmentObject]
                # print("Type: " + str(type(massAppointmentObjectList[week])))

def commit():
    with lock:
        saveAppointments(massAppointmentObjectList)
        appointmentConn.commit()
        massAppointmentObjectList.clear()

def close():
    appointmentConn.close()