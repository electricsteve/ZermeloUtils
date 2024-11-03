import json
# Appointment class
# Fields: id,appointmentInstance,start,end,startTimeSlot,endTimeSlot,branch,type,groupsInDepartments,locationsOfBranch,optional,valid,cancelled,cancelledReason,modified,teacherChanged,groupChanged,locationChanged,timeChanged,moved,created,hidden,changeDescription,schedulerRemark,content,lastModified,new,choosableInDepartments,choosableInDepartmentCodes,extraStudentSource,onlineLocationUrl,expectedStudentCount,expectedStudentCountOnline,udmUUID,creator,onlineStudents,appointmentLastModified,remark,availableSpace,subjects,teachers,onlineTeachers
# Types: id : int, appointmentInstance : AppointmentInstanceEntity, start : int, end : int, startTimeSlot : int, endTimeSlot : int, branch : BranchEntity, type : str, groupsInDepartments : list[int], locationsOfBranch : list[int], optional : bool, valid : bool, cancelled : bool, cancelledReason : str, modified : bool, teacherChanged : bool, groupChanged : bool, locationChanged : bool, timeChanged : bool, moved : bool, created : int, hidden : bool, changeDescription : str, schedulerRemark : str, content : str, lastModified : int, new : bool, choosableInDepartments : list[int], choosableInDepartmentCodes : list[str], extraStudentSource : str, onlineLocationUrl : str, expectedStudentCount : int, expectedStudentCountOnline : int, udmUUID : str, creator : str, onlineStudents : list[str], appointmentLastModified : int, remark : str, availableSpace : int, subjects : list[str], teachers : list[str], onlineTeachers : list[str]
class Appointment:
    def __init__(self, appointment):
        for field in ['id', 'appointmentInstance', 'start', 'end', 'startTimeSlot', 'endTimeSlot', 'branch', 'type', 'groupsInDepartments', 'locationsOfBranch', 'optional', 'valid', 'cancelled', 'cancelledReason', 'modified', 'teacherChanged', 'groupChanged', 'locationChanged', 'timeChanged', 'moved', 'created', 'hidden', 'changeDescription', 'schedulerRemark', 'content', 'lastModified', 'new', 'choosableInDepartments', 'choosableInDepartmentCodes', 'extraStudentSource', 'onlineLocationUrl', 'expectedStudentCount', 'expectedStudentCountOnline', 'udmUUID', 'creator', 'onlineStudents', 'appointmentLastModified', 'remark', 'availableSpace', 'subjects', 'teachers', 'onlineTeachers', 'online']:
            if field not in appointment:
                appointment[field] = None
        self.id = appointment['id']
        self.appointmentInstance = appointment['appointmentInstance']
        self.start = appointment['start']
        self.end = appointment['end']
        self.startTimeSlot = appointment['startTimeSlot']
        self.endTimeSlot = appointment['endTimeSlot']
        self.branch = appointment['branch']
        self.type = appointment['type']
        self.groupsInDepartments = appointment['groupsInDepartments']
        self.locationsOfBranch = appointment['locationsOfBranch']
        self.optional = appointment['optional']
        self.valid = appointment['valid']
        self.cancelled = appointment['cancelled']
        self.cancelledReason = appointment['cancelledReason']
        self.modified = appointment['modified']
        self.teacherChanged = appointment['teacherChanged']
        self.groupChanged = appointment['groupChanged']
        self.locationChanged = appointment['locationChanged']
        self.timeChanged = appointment['timeChanged']
        self.moved = appointment['moved']
        self.created = appointment['created']
        self.hidden = appointment['hidden']
        self.changeDescription = appointment['changeDescription']
        self.schedulerRemark = appointment['schedulerRemark']
        self.content = appointment['content']
        self.lastModified = appointment['lastModified']
        self.new = appointment['new']
        self.choosableInDepartments = appointment['choosableInDepartments']
        self.choosableInDepartmentCodes = appointment['choosableInDepartmentCodes']
        self.extraStudentSource = appointment['extraStudentSource']
        self.onlineLocationUrl = appointment['onlineLocationUrl']
        self.expectedStudentCount = appointment['expectedStudentCount']
        self.expectedStudentCountOnline = appointment['expectedStudentCountOnline']
        self.udmUUID = appointment['udmUUID']
        self.creator = appointment['creator']
        self.onlineStudents = appointment['onlineStudents']
        self.appointmentLastModified = appointment['appointmentLastModified']
        self.remark = appointment['remark']
        self.availableSpace = appointment['availableSpace']
        self.subjects = appointment['subjects']
        self.teachers = appointment['teachers']
        self.onlineTeachers = appointment['online']

    def __str__(self):
        return f'id: {self.id} appointmentInstance: {self.appointmentInstance} start: {self.start} end: {self.end} startTimeSlot: {self.startTimeSlot} endTimeSlot: {self.endTimeSlot} branch: {self.branch} type: {self.type} groupsInDepartments: {self.groupsInDepartments} locationsOfBranch: {self.locationsOfBranch} optional: {self.optional} valid: {self.valid} cancelled: {self.cancelled} cancelledReason: {self.cancelledReason} modified: {self.modified} teacherChanged: {self.teacherChanged} groupChanged: {self.groupChanged} locationChanged: {self.locationChanged} timeChanged: {self.timeChanged} moved: {self.moved} created: {self.created} hidden: {self.hidden} changeDescription: {self.changeDescription} schedulerRemark: {self.schedulerRemark} content: {self.content} lastModified: {self.lastModified} new: {self.new} choosableInDepartments: {self.choosableInDepartments} choosableInDepartmentCodes: {self.choosableInDepartmentCodes} extraStudentSource: {self.extraStudentSource} onlineLocationUrl: {self.onlineLocationUrl} expectedStudentCount: {self.expectedStudentCount} expectedStudentCountOnline: {self.expectedStudentCountOnline} udmUUID: {self.udmUUID} creator: {self.creator} onlineStudents: {self.onlineStudents} appointmentLastModified: {self.appointmentLastModified} remark: {self.remark} availableSpace: {self.availableSpace} subjects: {self.subjects} teachers: {self.teachers} onlineTeachers: {self.onlineTeachers}'

    def __repr__(self):
        return self.__str__()

    # Lists: groupsInDepartments, locationsOfBranch, choosableInDepartments, choosableInDepartmentCodes, onlineStudents, subjects, teachers, onlineTeachers
    def to_tuple(self):
        return self.id, self.appointmentInstance, self.start, self.end, self.startTimeSlot, self.endTimeSlot, self.branch, self.type, repr(self.groupsInDepartments), repr(self.locationsOfBranch), self.optional, self.valid, self.cancelled, self.cancelledReason, self.modified, self.teacherChanged, self.groupChanged, self.locationChanged, self.timeChanged, self.moved, self.created, self.hidden, self.changeDescription, self.schedulerRemark, self.content, self.lastModified, self.new, repr(self.choosableInDepartments), repr(self.choosableInDepartmentCodes), self.extraStudentSource, self.onlineLocationUrl, self.expectedStudentCount, self.expectedStudentCountOnline, self.udmUUID, self.creator, repr(self.onlineStudents), self.appointmentLastModified, self.remark, self.availableSpace, repr(self.subjects), repr(self.teachers), repr(self.onlineTeachers)