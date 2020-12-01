import pymongo
import pprint
import sys

from pymongo import MongoClient
client = MongoClient('localhost', 27017)

db = client.SirenDB
restreams = db.TestRestreams
users = db.TestUsers

def addRestream(restreamID, color, messageID, metaTitle, event, raceDate, lead):
    race = { 'restreamID': restreamID,
             'color': color,
             'messageID': messageID,
             'displayTitle': metaTitle,
             'event': event['name'],
             'time': event['startTime'],
             'date': raceDate,
             'channel': event['channel'],
             'openedBy': lead,
             'commentary1': '',
             'commentary2': '',
             'tracker': '',
             'restreamer': '',
             'status': 'Open'
            }
    restreams.insert_one(race)

def getRestreamField(restreamID, field):
    return restreams.find_one({'restreamID': restreamID})[field]

def setRestreamField(restreamID, field, value):
    restreams.find_one_and_update({'restreamID': restreamID}, {'$set': {field: value}})

def doesRestreamExist(restreamID):
    if restreams.count_documents({'restreamID': restreamID}):
        return True
    else:
        return False

def isRestreamOpen(restreamID):
    if restreams.find_one({'restreamID': restreamID})['status'] == 'Open':
        return True
    else:
        return False

def addUser(username, id, mention):
    user = { 'username': username,
             'id': id,
             'mention': mention,
             'lastAssigned': '',
             'hasRM': '',
             'hasRGBLB': '',
             'note': ''
            }
    users.insert_one(user)

def setUserField(username, field, value):
    users.find_one_and_update({'username': username}, {'$set': {field: value}})

def getUserField(username, field):
    return users.find_one({'username': username})[field]

def doesUserExist(username):
    if users.count_documents({'username': username}):
        return True
    else:
        return False
