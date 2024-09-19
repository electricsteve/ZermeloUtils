import os
import requests
import json
from dotenv import load_dotenv, find_dotenv, get_key
import dotenv
import datetime

dotenv_path = find_dotenv()

school = get_key(dotenv_path,"SCHOOL")
schoolInSchoolYear = get_key(dotenv_path,"SCHOOLYEAR")
authorization = get_key(dotenv_path,"AUTHORIZATION")

headers = {
    "Authorization": authorization
}

base_url = f"https://{school}.zportal.nl/api/v3/"
if os.path.isdir("logs") == False:
    os.mkdir("logs")

def get_students():
    data = get_endpoint("studentsindepartments", f"schoolInSchoolYear={schoolInSchoolYear}&fields=id,student,departmentOfBranch,mentorGroup,mainGroup,groupInDepartments,fullName,schoolInSchoolYear,firstName,lastName,departmentOfBranchCode,mainGroupName,prefix")
    return data

def get_teachers():
    data = get_endpoint("contracts", f"schoolInSchoolYear={schoolInSchoolYear}&fields=id,employee,schoolInSchoolYear,isMainContract,mainBranchOfSchool,schoolYear,schoolInSchoolYearName,lastName,school,schoolName,employeeNumber,postedBranches,prefix")
    return data

def get_endpoint(endpoint, parameters):
    url = base_url + endpoint + "?" + parameters
    req = requests.get(url, headers=headers)
    json_data = json.loads(req.text)
    messagefile = "logs/message" + datetime.datetime.now().strftime("-%Y%m%d-%H%M%S%f") + ".json"
    json_data["request"] = {
        "url": url,
        "headers": headers
    }
    with open(messagefile, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    response = json_data["response"]
    if response["status"] != 200:
        print("Error: ", response["message"])
        print("Error response saved in: ", messagefile)
        raise Exception(response["message"])
    return response["data"]