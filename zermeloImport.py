import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

school = os.getenv("SCHOOL")
schoolInSchoolYear = os.getenv("SCHOOLYEAR")
authorization = os.getenv("AUTHORIZATION")
cookie = os.getenv("COOKIE")

url = f"https://{school}.zportal.nl/api/v3/studentsindepartments?schoolInSchoolYear={schoolInSchoolYear}&fields=id,student,departmentOfBranch,mentorGroup,mainGroup,groupInDepartments,fullName,schoolInSchoolYear,firstName,lastName,departmentOfBranchCode,mainGroupName,prefix"
headers = {
    "Authorization": authorization
}
req = requests.get(url, headers=headers)
json_data = json.loads(req.text)

with open('message.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)

response = json_data["response"]
for keyValue in dict(response):
    if keyValue != "data":
        response.pop(keyValue)

with open('leerlingen.json', 'w', encoding='utf-8') as f:
    json.dump(response, f, ensure_ascii=False, indent=4)