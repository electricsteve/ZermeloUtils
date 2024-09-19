import sqlite3
from Student import Student
import Zermelo

list_of_students = Zermelo.get_students()

print("Number of students: ", len(list_of_students))
# Create a connection to the database
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS LEERLINGEN")
table = """ CREATE TABLE LEERLINGEN (
    id INTEGER PRIMARY KEY,
    student TEXT NOT NULL,
    departmentOfBranch INTEGER NOT NULL,
    mentorGroup INTEGER,
    mainGroup INTEGER NOT NULL,
    groupInDepartments TEXT,
    fullName TEXT NOT NULL,
    schoolInSchoolYear INTEGER NOT NULL,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    departmentOfBranchCode TEXT NOT NULL,
    mainGroupName TEXT NOT NULL,
    prefix TEXT
        ); """
c.execute(table)

for student in list_of_students:
    studentClass = Student(student)
    c.execute("INSERT INTO LEERLINGEN VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", studentClass.to_tuple())
    print(studentClass)

conn.commit()
conn.close()