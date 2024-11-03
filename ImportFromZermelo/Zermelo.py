import datetime
import json
import os

import requests
from dotenv import find_dotenv, get_key

dotenv_path = find_dotenv()

school = get_key(dotenv_path,"SCHOOL")
schoolInSchoolYear = get_key(dotenv_path,"SCHOOLYEAR")
authorization = get_key(dotenv_path,"AUTHORIZATION")

headers = {
    "Authorization": authorization
}

base_url = f"https://{school}.zportal.nl/api/v3/"
if not os.path.isdir("./logs"):
    os.mkdir("./logs")
if not os.path.isdir("./logs/messages"):
    os.mkdir("./logs/messages")

def get_students():
    data = get_endpoint("studentsindepartments", f"schoolInSchoolYear={schoolInSchoolYear}&fields=id,student,departmentOfBranch,mentorGroup,mainGroup,groupInDepartments,fullName,schoolInSchoolYear,firstName,lastName,departmentOfBranchCode,mainGroupName,prefix")
    return data

def get_teachers():
    data = get_endpoint("contracts", f"schoolInSchoolYear={schoolInSchoolYear}&fields=id,employee,schoolInSchoolYear,isMainContract,mainBranchOfSchool,schoolYear,schoolInSchoolYearName,lastName,school,schoolName,employeeNumber,postedBranches,prefix")
    return data

def get_locations():
    data = get_endpoint("locationofbranches", f"schoolInSchoolYear={schoolInSchoolYear}&fields=id,name,parentteachernightCapacity,courseCapacity,supportsConcurrentAppointments,allowMeetings,branchOfSchool,secondaryBranches,schoolInSchoolYear")
    return data
def get_groups():
    data = get_endpoint("groupindepartments", f"schoolInSchoolYear={schoolInSchoolYear}&fields=id,isMainGroup,isMentorGroup,departmentOfBranch,name,extendedName")
    return data

def get_appointments(startWeek, endWeek, user, modifiedSince : int = None):
    start = int(datetime.datetime.strptime(f"2024-{startWeek}-1", "%Y-%W-%w").timestamp())
    end = int(datetime.datetime.strptime(f"2024-{endWeek + 1}-1", "%Y-%W-%w").timestamp())
    extraFields = ""
    if modifiedSince is not None: extraFields += f"&modifiedSince={modifiedSince}"
    data = get_endpoint("appointments", f"user={user}{extraFields}&start={start}&end={end}&fields=id,appointmentInstance,start,end,startTimeSlot,endTimeSlot,branch,type,groupsInDepartments,locationsOfBranch,optional,valid,cancelled,cancelledReason,modified,teacherChanged,groupChanged,locationChanged,timeChanged,moved,created,hidden,changeDescription,schedulerRemark,content,lastModified,new,choosableInDepartments,choosableInDepartmentCodes,extraStudentSource,onlineLocationUrl,expectedStudentCount,expectedStudentCountOnline,udmUUID,creator,onlineStudents,appointmentLastModified,remark,availableSpace,subjects,teachers,onlineTeachers")
    return data

def get_endpoint(endpoint, parameters):
    url = base_url + endpoint + "?" + parameters
    req = requests.get(url, headers=headers)
    json_data = json.loads(req.text)
    messagefile = "./logs/messages/message" + datetime.datetime.now().strftime("-%Y%m%d-%H%M%S%f") + ".json"
    json_data["request"] = {
        "url": url,
        "headers": headers
    }
    with open(messagefile, 'w', encoding='utf-8') as f:
        # noinspection PyTypeChecker
        json.dump(json_data, f, ensure_ascii=False, indent=4, sort_keys=True)
    response = json_data["response"]
    if response["status"] != 200:
        print("Error: ", response["message"])
        print("Error response saved in: ", messagefile)
        raise Exception(str(response["status"]) + response["message"])
    return response["data"]