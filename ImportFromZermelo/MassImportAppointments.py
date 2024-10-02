import sqlite3
import sys
from os.path import dirname, abspath
sys.path.append(abspath(dirname(dirname(__file__))))
import ImportAppointments

args = sys.argv

if len(args) < 2:
    print("Please provide action")
    sys.exit()

action = args[1]
if action == "allDatabase":
    conn = sqlite3.connect('./database.db')
    c = conn.cursor()
    c.execute("SELECT student FROM STUDENTS")
    students = c.fetchall()
    for student in students:
        print("Importing appointments for: ", student[0])
        ImportAppointments.ImportAppointments(student[0], 1, 52)
    conn.close()
    ImportAppointments.close()
elif action == "students":
    # Range
    if len(args) < 4:
        print("Please provide student range")
        sys.exit()
    studentsStart = args[2]
    studentsEnd = args[3]
    for i in range(int(studentsStart), int(studentsEnd) + 1):
        print("Importing appointments for: ", i)
        ImportAppointments.ImportAppointments(i, 1, 52)
    ImportAppointments.close()