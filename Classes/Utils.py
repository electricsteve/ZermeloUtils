import ast
import sqlite3
import re
from datetime import datetime
from enum import Enum
from Classes.Student import Student
from Classes.Teacher import Teacher
from Classes.Group import Group
from Classes.Appointment import Appointment

def parseWeek(weekStr : str) -> tuple[int, int]:
    """
    Parse a week string to a tuple of week and year
    :param weekStr: Week string formatted as "2025-03", "03" (meaning current year) or "3"
    :return: Tuple of week and year
    """
    # Verify if week string is correctly formatted
    if re.search(r"^(\d{4})-(\d{1,2})$", weekStr):
        ...
    elif re.search(r"^(\d{1,2})$", weekStr):
        ...
    else:
        raise ValueError("Week string is not formatted correctly")

    if "-" in weekStr:
        year, week = weekStr.split("-")
        year = int(year)
        week = int(week)
    else:
        week = int(weekStr)
        year = datetime.now().year

    if week > 52 or week < 1:
        raise ValueError("Week number is higher than 52 or lower than 1")
    if year < 1970 or year > 2038:
        raise ValueError("Year is not withing unix timestamp range")
    return week, year


class UserType(Enum):
    STUDENT = "student"
    TEACHER = "teacher"

def user_exists(userId, userType : UserType):
    return get_user(userId, userType) is not None

def get_user(userId, userType : UserType) -> Student | Teacher | None:
    conn = sqlite3.connect('./database.db')
    cursor = conn.cursor()
    match userType:
        case UserType.STUDENT:
            cursor.execute('SELECT * FROM STUDENTS WHERE student = ?', (userId,))
            return Student.from_tuple(cursor.fetchone())
        case UserType.TEACHER:
            cursor.execute('SELECT * FROM TEACHERS WHERE employee = ?', (userId,))
            return Teacher.from_tuple(cursor.fetchone())
        case _:
            return None

def getAppointments() -> list[Appointment]:
    conn = sqlite3.connect('./appointments.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM EVERYTHING')
    return [Appointment.from_tuple(row) for row in cursor.fetchall()]

def getStudents() -> list[Student]:
    conn = sqlite3.connect('./database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM STUDENTS')
    return [Student.from_tuple(row) for row in cursor.fetchall()]

def getTeachers() -> list[Teacher]:
    conn = sqlite3.connect('./database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM TEACHERS')
    return [Teacher.from_tuple(row) for row in cursor.fetchall()]

def getGroups() -> list[Group]:
    conn = sqlite3.connect('./database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM GROUPS')
    return [Group.from_tuple(row) for row in cursor.fetchall()]

def getStudentsInGroup(group) -> list[Student]:
    conn = sqlite3.connect('./database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM STUDENTS WHERE groupInDepartments LIKE ?', (f'%{group}%',))
    return [Student.from_tuple(row) for row in cursor.fetchall()]

def getStudentSchedule(student : Student) -> list[Appointment]:
    conn = sqlite3.connect('./appointments.db')
    cursor = conn.cursor()
    conn2 = sqlite3.connect('./database.db')
    cursor2 = conn2.cursor()

    cursor2.execute('SELECT groupInDepartments FROM STUDENTS where student = ?', (student.student,))
    groups = ast.literal_eval(cursor2.fetchone()[0])
    appointments = []
    for group in groups:
        cursor.execute('SELECT * FROM EVERYTHING WHERE groupsInDepartments like ?', (f'%{group}%',))
        appointments += [Appointment.from_tuple(row) for row in cursor.fetchall()]

    return appointments