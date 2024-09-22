# Group object
# Fields: id,isMainGroup,isMentorGroup,departmentOfBranch,name,extendedName
# Types: id : int,isMainGroup : bool,isMentorGroup : bool,departmentOfBranch : int,name : str,extendedName : str
class Group:
    def __init__(self, group):
        self.id = group["id"]
        self.isMainGroup = group["isMainGroup"]
        self.isMentorGroup = group["isMentorGroup"]
        self.departmentOfBranch = group["departmentOfBranch"]
        self.name = group["name"]
        self.extendedName = group["extendedName"]

    def __str__(self):
        return f'Id: {self.id} Is_Main_Group: {self.isMainGroup} Is_Mentor_Group: {self.isMentorGroup} Department_Of_Branch: {self.departmentOfBranch} Name: {self.name} Extended_Name: {self.extendedName}'

    def __repr__(self):
        return self.__str__()

    def to_tuple(self):
        return self.id, self.isMainGroup, self.isMentorGroup, self.departmentOfBranch, self.name, self.extendedName
