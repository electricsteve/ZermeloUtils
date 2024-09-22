import sqlite3
from Classes.Appointment import Appointment

import Zermelo

# Create a connection to the database
conn = sqlite3.connect('../appointments.db')
c = conn.cursor()

def ImportAppointments(user):
    list_of_appointments = Zermelo.get_appointments(39, 39, user)
    print("Number of appointments: ", len(list_of_appointments))
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
    c.execute(table)
    for appointment in list_of_appointments:
        appointmentObject = Appointment(appointment)
        c.execute(f"INSERT OR REPLACE INTO '{user}' VALUES ({', '.join(['?'] * 42)})", appointmentObject.to_tuple())
        print(appointmentObject)
    conn.commit()

def close():
    conn.close()