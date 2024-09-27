import ast
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
        self.groupInDepartments = student["groupInDepartments"]
        self.fullName = student["fullName"]
        self.schoolInSchoolYear = student["schoolInSchoolYear"]
        self.firstName = student["firstName"]
        self.lastName = student["lastName"]
        self.departmentOfBranchCode = student["departmentOfBranchCode"]
        self.mainGroupName = student["mainGroupName"]
        self.prefix = student["prefix"]

    @staticmethod
    def from_tuple(t):
        student = {}
        student["id"] = t[0]
        student["student"] = t[1]
        student["departmentOfBranch"] = t[2]
        student["mentorGroup"] = t[3]
        student["mainGroup"] = t[4]
        student["groupInDepartments"] = ast.literal_eval(t[5])
        student["fullName"] = t[6]
        student["schoolInSchoolYear"] = t[7]
        student["firstName"] = t[8]
        student["lastName"] = t[9]
        student["departmentOfBranchCode"] = t[10]
        student["mainGroupName"] = t[11]
        student["prefix"] = t[12]
        return Student(student)

    def __str__(self):
        return f'Id: {self.id} Student: {self.student} Department_Of_branch: {self.departmentOfBranch} Mentor_Group: {self.mentorGroup} Main_Group: {self.mainGroup} Group_In_Departments: {self.groupInDepartments} Full_Name: {self.fullName} School_In_School_Year: {self.schoolInSchoolYear} First_Name: {self.firstName} Last_Name: {self.lastName} Department_Of_Branch_Code: {self.departmentOfBranchCode} Main_Group_Name: {self.mainGroupName} Prefix: {self.prefix}'

    def __repr__(self):
        return self.__str__()

    def to_tuple(self):
        return self.id, self.student, self.departmentOfBranch, self.mentorGroup, self.mainGroup, str(self.groupInDepartments), self.fullName, self.schoolInSchoolYear, self.firstName, self.lastName, self.departmentOfBranchCode, self.mainGroupName, self.prefix

    def in_common(self, student, conn):
        common = []
        if self.id == student.id:
            common.append("Same student")
            return common
        c = conn.cursor()
        for group in self.groupInDepartments:
            if group in student.groupInDepartments:
                c.execute("SELECT extendedName FROM GROUPS WHERE id=?", (group,))
                common.append(c.fetchone()[0])
        return common