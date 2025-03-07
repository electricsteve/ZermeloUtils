import sqlite3
import sys
from os.path import dirname, abspath
from time import sleep

sys.path.append(abspath(dirname(dirname(__file__))))
import ImportAppointments
import threading

done = False


def splitList(inputList, n):
    for i in range(0, len(inputList), n):
        yield inputList[i:i + n]

def importThread(inputStudents, start, end):
    for student in inputStudents:
        ImportAppointments.ImportAppointments(student[0], start, end)

def savingThread():
    while True:
        print("Waiting 30 seconds before saving")
        sleep(30)
        print("Committing")
        ImportAppointments.commit()
        print("Done saving")
        sleep(5)
        if done:
            break

if __name__ == "__main__":
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
        ImportAppointments.setMass(True)
        numberOfThreads = 10
        lists = list(splitList(students, len(students) // numberOfThreads))
        if numberOfThreads > len(lists):
            numberOfThreads = len(lists)
        threads = []
        for i in range(numberOfThreads):
            threads.append(threading.Thread(target=importThread, args=(lists[i], 1, 52)))
            threads[i].start()
        saving = threading.Thread(target=savingThread)
        saving.start()
        # wait for threads to finish
        for i in range(numberOfThreads):
            threads[i].join()
        done = True
        saving.join()
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
        ImportAppointments.commit()
        ImportAppointments.close()



def close():
    ImportAppointments.commit()
    ImportAppointments.close()