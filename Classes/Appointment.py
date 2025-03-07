import ast
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

    @staticmethod
    def from_tuple(t):
        return Appointment({
            'id': t[0],
            'appointmentInstance': t[1],
            'start': t[2],
            'end': t[3],
            'startTimeSlot': t[4],
            'endTimeSlot': t[5],
            'branch': t[6],
            'type': t[7],
            'groupsInDepartments': ast.literal_eval(t[8]),
            'locationsOfBranch': ast.literal_eval(t[9]),
            'optional': t[10],
            'valid': t[11],
            'cancelled': t[12],
            'cancelledReason': t[13],
            'modified': t[14],
            'teacherChanged': t[15],
            'groupChanged': t[16],
            'locationChanged': t[17],
            'timeChanged': t[18],
            'moved': t[19],
            'created': t[20],
            'hidden': t[21],
            'changeDescription': t[22],
            'schedulerRemark': t[23],
            'content': t[24],
            'lastModified': t[25],
            'new': t[26],
            'choosableInDepartments': ast.literal_eval(t[27]),
            'choosableInDepartmentCodes': ast.literal_eval(t[28]),
            'extraStudentSource': t[29],
            'onlineLocationUrl': t[30],
            'expectedStudentCount': t[31],
            'expectedStudentCountOnline': t[32],
            'udmUUID': t[33],
            'creator': t[34],
            'onlineStudents': ast.literal_eval(t[35]),
            'appointmentLastModified': t[36],
            'remark': t[37],
            'availableSpace': t[38],
            'subjects': ast.literal_eval(t[39]),
            'teachers': ast.literal_eval(t[40]),
            'online': ast.literal_eval(t[41])
        })

    def __str__(self):
        return f'id: {self.id} appointmentInstance: {self.appointmentInstance} start: {self.start} end: {self.end} startTimeSlot: {self.startTimeSlot} endTimeSlot: {self.endTimeSlot} branch: {self.branch} type: {self.type} groupsInDepartments: {self.groupsInDepartments} locationsOfBranch: {self.locationsOfBranch} optional: {self.optional} valid: {self.valid} cancelled: {self.cancelled} cancelledReason: {self.cancelledReason} modified: {self.modified} teacherChanged: {self.teacherChanged} groupChanged: {self.groupChanged} locationChanged: {self.locationChanged} timeChanged: {self.timeChanged} moved: {self.moved} created: {self.created} hidden: {self.hidden} changeDescription: {self.changeDescription} schedulerRemark: {self.schedulerRemark} content: {self.content} lastModified: {self.lastModified} new: {self.new} choosableInDepartments: {self.choosableInDepartments} choosableInDepartmentCodes: {self.choosableInDepartmentCodes} extraStudentSource: {self.extraStudentSource} onlineLocationUrl: {self.onlineLocationUrl} expectedStudentCount: {self.expectedStudentCount} expectedStudentCountOnline: {self.expectedStudentCountOnline} udmUUID: {self.udmUUID} creator: {self.creator} onlineStudents: {self.onlineStudents} appointmentLastModified: {self.appointmentLastModified} remark: {self.remark} availableSpace: {self.availableSpace} subjects: {self.subjects} teachers: {self.teachers} onlineTeachers: {self.onlineTeachers}'

    def __repr__(self):
        return self.__str__()

    # Lists: groupsInDepartments, locationsOfBranch, choosableInDepartments, choosableInDepartmentCodes, onlineStudents, subjects, teachers, onlineTeachers
    def to_tuple(self):
        return self.id, self.appointmentInstance, self.start, self.end, self.startTimeSlot, self.endTimeSlot, self.branch, self.type, repr(self.groupsInDepartments), repr(self.locationsOfBranch), self.optional, self.valid, self.cancelled, self.cancelledReason, self.modified, self.teacherChanged, self.groupChanged, self.locationChanged, self.timeChanged, self.moved, self.created, self.hidden, self.changeDescription, self.schedulerRemark, self.content, self.lastModified, self.new, repr(self.choosableInDepartments), repr(self.choosableInDepartmentCodes), self.extraStudentSource, self.onlineLocationUrl, self.expectedStudentCount, self.expectedStudentCountOnline, self.udmUUID, self.creator, repr(self.onlineStudents), self.appointmentLastModified, self.remark, self.availableSpace, repr(self.subjects), repr(self.teachers), repr(self.onlineTeachers)