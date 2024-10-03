import sqlite3
import sys
from os.path import dirname, abspath
sys.path.append(abspath(dirname(dirname(__file__))))
import ImportAppointments
import threading

args = sys.argv

if len(args) < 2:
    print("Please provide action")
    sys.exit()


def splitList(list, n):
    for i in range(0, len(list), n):
        yield list[i:i + n]

def importThread(students, start, end):
    for student in students:
        ImportAppointments.ImportAppointments(student[0], start, end)

action = args[1]
if action == "allDatabase":
    conn = sqlite3.connect('./database.db')
    c = conn.cursor()
    c.execute("SELECT student FROM STUDENTS")
    students = c.fetchall()
    ImportAppointments.setMass(True)
    numberOfThreads = 10
    lists = list(splitList(students, len(students) // numberOfThreads))
    if numberOfThreads > len(lists):
        numberOfThreads = len(lists)
    threads = []
    for i in range(numberOfThreads):
        threads.append(threading.Thread(target=importThread, args=(lists[i], 1, 52)))
        threads[i].start()
    # wait for threads to finish
    for i in range(numberOfThreads):
        threads[i].join()
    conn.close()
    ImportAppointments.commit()
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
