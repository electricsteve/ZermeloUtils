import sqlite3
from Classes.Teacher import Teacher
import Zermelo

list_of_teachers = Zermelo.get_teachers()

print("Number of teachers: ", len(list_of_teachers))
# Create a connection to the database
conn = sqlite3.connect('../database.db')
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS TEACHERS")
# Types: id : int,employee : str,schoolInSchoolYear : int,isMainContract : bool,mainBranchOfSchool : int,schoolYear : 2024,schoolInSchoolYearName : str,lastName : str,school : int,schoolName : str,employeeNumber : null,postedBranches : null array,prefix : str
table = """ CREATE TABLE TEACHERS (
    id INTEGER PRIMARY KEY,
    employee TEXT,
    schoolInSchoolYear INTEGER,
    isMainContract BOOLEAN,
    mainBranchOfSchool INTEGER,
    schoolYear INTEGER,
    schoolInSchoolYearName TEXT,
    lastName TEXT,
    school INTEGER,
    schoolName TEXT,
    employeeNumber TEXT,
    postedBranches TEXT,
    prefix TEXT
        ); """
c.execute(table)

for teacher in list_of_teachers:
    teacherObject = Teacher(teacher)
    c.execute("INSERT INTO TEACHERS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", teacherObject.to_tuple())
    print(teacherObject)

conn.commit()
conn.close()