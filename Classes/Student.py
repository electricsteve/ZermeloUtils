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
        return self.id, self.student, self.departmentOfBranch, self.mentorGroup, self.mainGroup, self.groupInDepartments, self.fullName, self.schoolInSchoolYear, self.firstName, self.lastName, self.departmentOfBranchCode, self.mainGroupName, self.prefix
