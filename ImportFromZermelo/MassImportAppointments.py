import sqlite3
import sys
from os.path import dirname, abspath
from time import sleep

sys.path.append(abspath(dirname(dirname(__file__))))
import ImportAppointments
import threading

args = sys.argv

if len(args) < 2:
    print("Please provide action")
    sys.exit()

getting = False
saving = False
condition = threading.Condition()

def splitList(list, n):
    for i in range(0, len(list), n):
        yield list[i:i + n]

def importThread(students, start, end):
    for student in students:
        if saving:
            print("Waiting for saving to be false")
        condition.wait_for(lambda: not saving)
        global getting
        print("Getting true")
        getting = True
        ImportAppointments.ImportAppointments(student[0], start, end)
        print("Done getting")
        getting = False

def savingThread():
    print("Saving thread started, waiting 30 seconds")
    sleep(30)
    print("Saving true")
    global saving
    saving = True
    print("Waiting for getting to be false")
    condition.wait_for(lambda: not getting)
    print("Getting is false")
    ImportAppointments.commit()
    sleep(5)
    print("Done saving")
    saving = False

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
    threading.Thread(target=savingThread).start()
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
