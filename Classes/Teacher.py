# Teacher object
# Fields: id,employee,schoolInSchoolYear,isMainContract,mainBranchOfSchool,schoolYear,schoolInSchoolYearName,lastName,school,schoolName,employeeNumber,postedBranches,prefix
# Types: id : int,employee : str,schoolInSchoolYear : int,isMainContract : bool,mainBranchOfSchool : int,schoolYear : 2024,schoolInSchoolYearName : str,lastName : str,school : int,schoolName : str,employeeNumber : null,postedBranches : null array,prefix : str
class Teacher:
    def __init__(self, teacher):
        self.id = teacher["id"]
        self.employee = teacher["employee"]
        self.schoolInSchoolYear = teacher["schoolInSchoolYear"]
        self.isMainContract = teacher["isMainContract"]
        self.mainBranchOfSchool = teacher["mainBranchOfSchool"]
        self.schoolYear = teacher["schoolYear"]
        self.schoolInSchoolYearName = teacher["schoolInSchoolYearName"]
        self.lastName = teacher["lastName"]
        self.school = teacher["school"]
        self.schoolName = teacher["schoolName"]
        self.employeeNumber = teacher["employeeNumber"]
        if teacher["postedBranches"] is None:
            self.postedBranches = "[]"
        else:
            temp = "[ " + ", ".join(str(x) for x in teacher["postedBranches"]) + " ]"
            self.postedBranches = temp
        self.prefix = teacher["prefix"]

    @staticmethod
    def from_tuple(t):
        teacher = {}
        teacher["id"] = t[0]
        teacher["employee"] = t[1]
        teacher["schoolInSchoolYear"] = t[2]
        teacher["isMainContract"] = t[3]
        teacher["mainBranchOfSchool"] = t[4]
        teacher["schoolYear"] = t[5]
        teacher["schoolInSchoolYearName"] = t[6]
        teacher["lastName"] = t[7]
        teacher["school"] = t[8]
        teacher["schoolName"] = t[9]
        teacher["employeeNumber"] = t[10]
        teacher["postedBranches"] = t[11]
        teacher["prefix"] = t[12]
        return Teacher(teacher)

    def __str__(self):
        return f'Id: {self.id} Employee: {self.employee} School_In_School_Year: {self.schoolInSchoolYear} Is_Main_Contract: {self.isMainContract} Main_Branch_Of_School: {self.mainBranchOfSchool} School_Year: {self.schoolYear} School_In_School_Year_Name: {self.schoolInSchoolYearName} Last_Name: {self.lastName} School: {self.school} School_Name: {self.schoolName} Employee_Number: {self.employeeNumber} Posted_Branches: {self.postedBranches} Prefix: {self.prefix}'

    def __repr__(self):
        return self.__str__()

    def to_tuple(self):
        return self.id, self.employee, self.schoolInSchoolYear, self.isMainContract, self.mainBranchOfSchool, self.schoolYear, self.schoolInSchoolYearName, self.lastName, self.school, self.schoolName, self.employeeNumber, self.postedBranches, self.prefix

    def get_name(self):
        return self.employee