import sqlite3
from enum import Enum
from Classes.Student import Student
from Classes.Teacher import Teacher

class UserType(Enum):
    STUDENT = "student"
    TEACHER = "teacher"

def user_exists(userId, userType : UserType):
    return get_user(userId, userType) is not None

def get_user(userId, userType : UserType):
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