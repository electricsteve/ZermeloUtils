import json
import sqlite3

# Student object
# Fields: id,student,departmentOfBranch,mentorGroup,mainGroup,groupInDepartments,fullName,schoolInSchoolYear,firstName,lastName,departmentOfBranchCode,mainGroupName,prefix
# Types: id : int,student : string,departmentOfBranch : int,mentorGroup : int (nullable),mainGroup : int,groupInDepartments : int array,fullName : string,schoolInSchoolYear : int,firstName : string,lastName : string,departmentOfBranchCode : string,mainGroupName : string,prefix : string (nullable)
class Student:
    def __init__(self, student):
        self.id = student["id"]
        self.student = student["student"]
        self.departmentOfBranch = student["departmentOfBranch"]
        self.mentorGroup = student["mentorGroup"]
        self.mainGroup = student["mainGroup"]
        if student["groupInDepartments"] is None:
            self.groupInDepartments = "[]"
        else:
            temp = "[ " + ", ".join(str(x) for x in student["groupInDepartments"]) + " ]"
            self.groupInDepartments = temp
        self.fullName = student["fullName"]
        self.schoolInSchoolYear = student["schoolInSchoolYear"]
        self.firstName = student["firstName"]
        self.lastName = student["lastName"]
        self.departmentOfBranchCode = student["departmentOfBranchCode"]
        self.mainGroupName = student["mainGroupName"]
        self.prefix = student["prefix"]

    def __str__(self):
        return f'Id: {self.id} Student: {self.student} Department_Of_branch: {self.departmentOfBranch} Mentor_Group: {self.mentorGroup} Main_Group: {self.mainGroup} Group_In_Departments: {self.groupInDepartments} Full_Name: {self.fullName} School_In_School_Year: {self.schoolInSchoolYear} First_Name: {self.firstName} Last_Name: {self.lastName} Department_Of_Branch_Code: {self.departmentOfBranchCode} Main_Group_Name: {self.mainGroupName} Prefix: {self.prefix}'

    def __repr__(self):
        return self.__str__()

    def to_tuple(self):
        return (self.id, self.student, self.departmentOfBranch, self.mentorGroup, self.mainGroup, self.groupInDepartments, self.fullName, self.schoolInSchoolYear, self.firstName, self.lastName, self.departmentOfBranchCode, self.mainGroupName, self.prefix)
def read_students():
    with open('leerlingen.json', encoding='utf-8') as f:
        return json.load(f)

json_data = read_students()
list_of_students = json_data["data"]

print("Number of students: ", len(list_of_students))
# Create a connection to the database
conn = sqlite3.connect('leerlingen.db')
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