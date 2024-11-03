import json
from Classes import Utils
import os

'''
Config file format:
"trackedUsers": [ {"type": "student", "id": "12345"}, {"type": "teacher", "id": "dez"} ]

'''

configFile = 'trackedUsers.json'

if not os.path.isfile(configFile):
    with open(configFile, 'w') as file:
        # noinspection PyTypeChecker
        json.dump({"trackedUsers": []}, file)

def getTrackedUsers():
    with open(configFile, 'r') as f:
        config = json.load(f)
    return config['trackedUsers']

def getTrackedUsersByType(userType : Utils.UserType):
    with open(configFile, 'r') as f:
        config = json.load(f)
    return [user for user in config['trackedUsers'] if user['type'] == userType]

def addTrackedUser(userType, id):
    with open(configFile, 'r') as f:
        config = json.load(f)
    if isTrackedUser(userType, id):
        raise ValueError('User already tracked')
    config['trackedUsers'].append({"type": userType, "id": id})
    with open(configFile, 'w') as f:
        # noinspection PyTypeChecker
        json.dump(config, f)

def removeTrackedUser(userType, id):
    with open(configFile, 'r') as f:
        oldConfig = json.load(f)
    config = oldConfig.copy()
    config['trackedUsers'] = [user for user in config['trackedUsers'] if not (user['type'] == userType and user['id'] == id)]
    if len(config['trackedUsers']) == len(oldConfig['trackedUsers']):
        raise ValueError('User not on list')
    with open(configFile, 'w') as f:
        # noinspection PyTypeChecker
        json.dump(config, f)

def isTrackedUser(userType, id):
    with open(configFile, 'r') as f:
        config = json.load(f)
    return any([user for user in config['trackedUsers'] if user['type'] == userType and user['id'] == id])
