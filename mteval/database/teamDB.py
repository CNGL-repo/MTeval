from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime


client = MongoClient("localhost", 27017)
db = client.mteval

def addTeam(teamName, email, organisation, passwordHash, isAdmin = False, emailVerified = False, isActive = False):
	res = None
	team = db.teams.find_one({"teamName": teamName})
	if team != None:
		res = {
			"success": False,
			"reason": "Team username already exists"
		}
		return res
	team =db.teams.find_one({"email": email})
	if team != None:
		res = {
			"success": False,
			"reason": "Team email already exists"
		}
		return res

	team = {
		"teamName": teamName,
		"email": email, 
		"organisation": organisation,
		"passwordHash": passwordHash, 
		"isAdmin": isAdmin,
		"emailVerified": emailVerified,
		"isActive": isActive,
		"submissions":[]
	}

	db.teams.insert_one(team)
	res = {
		"success": True
	}
	return res

def editTeam(oldName, newName, email, organisation, passwordHash):
	db.teams.update_one(
	{"teamName": oldName}, 
	{"$set": {
		"teamName": newName,
		"email": email,
		"organisation": organisation,
		"passwordHash": passwordHash
	}
	})

def appendSub(filename, teamName, compId):

	date = datetime.datetime.now()
	db.teams.update_one({"teamName": teamName},
	    {"$push": 
        {"submissions": 
            {"filename": filename,
            "date": date,
            "compId": compId
            }
        }
    	})


def removeTeam(teamName):
	db.teams.delete_one({"teamName": teamName})

def getTeamByName(teamName):
	return db.teams.find_one({"teamName": teamName})

def getTeamByEmail(email):
	return db.teams.find_one({"email": email})

def getTeamById(teamId):
	return db.teams.find_one({"_id": ObjectId(teamId)})

def getPendingTeams():
	teams = db.teams.find({"isActive": False})
	res = []
	for team in teams:
		team["_id"] = str(team["_id"])
		res.append(team)
	return res

def getTeamList():
	teams = db.teams.find({"isActive": True, "isAdmin": False})
	res = []
	for team in teams:
		team["_id"] = str(team["_id"])
		res.append(team)
	return res

def getAdmin():
	return db.teams.find_one({"isAdmin": True})

def setEmailVerified(teamName):
	db.teams.update_one({"teamName": teamName}, {"$set": {"emailVerified": True}})

def acceptTeam(teamName):
	db.teams.update_one({"teamName": teamName}, {"$set": {"isActive": True}})
