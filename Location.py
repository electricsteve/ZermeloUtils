# Location object
# Fields: id,name,parentteachernightCapacity,courseCapacity,supportsConcurrentAppointments,allowMeetings,branchOfSchool,secondaryBranches,schoolInSchoolYear
# Types: id : int, name : string, parentteachernightCapacity : int, courseCapacity : int, supportsConcurrentAppointments : bool, allowMeetings : bool, branchOfSchool : int, secondaryBranches : list, schoolInSchoolYear : int
class Location:
    def __init__(self, location):
        self.id = location['id']
        self.name = location['name']
        self.parentTeacherNightCapacity = location['parentteachernightCapacity']
        self.courseCapacity = location['courseCapacity']
        self.supportsConcurrentAppointments = location['supportsConcurrentAppointments']
        self.allowMeetings = location['allowMeetings']
        self.branchOfSchool = location['branchOfSchool']
        if location['secondaryBranches'] is None:
            self.secondaryBranches = "[]"
        else:
            temp = "[ " + ", ".join(str(x) for x in location['secondaryBranches']) + " ]"
            self.secondaryBranches = temp
        self.schoolInSchoolYear = location['schoolInSchoolYear']

    def __str__(self):
        return f'ID: {self.id}, Name: {self.name}, Parent Teacher Night Capacity: {self.parentTeacherNightCapacity}, Course Capacity: {self.courseCapacity}, Supports Concurrent Appointments: {self.supportsConcurrentAppointments}, Allow Meetings: {self.allowMeetings}, Branch of School: {self.branchOfSchool}, Secondary Branches: {self.secondaryBranches}, School in School Year: {self.schoolInSchoolYear}'

    def __repr__(self):
        return self.__str__()

    def to_tuple(self):
        return self.id, self.name, self.parentTeacherNightCapacity, self.courseCapacity, self.supportsConcurrentAppointments, self.allowMeetings, self.branchOfSchool, self.secondaryBranches, self.schoolInSchoolYear
