from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient("localhost", 27017)
db = client.mteval

def addTeam(teamName, email, organisation, passwordHash, isAdmin = False, isVerified = False, isActive = False):
	res = None
	team = db.teams.find_one({"teamName": teamName})
	if team != None:
		res = {
			"success": False,
			"reason": "Team already exists"
		}
		return res
	team = {
		"teamName": teamName,
		"email": email, 
		"organisation": organisation,
		"passwordHash": passwordHash, 
		"isAdmin": isAdmin,
		"isVerified": isVerified,
		"isActive": isActive
	}

	db.teams.insert_one(team)
	res = {
		"success": True
	}
	return res

def getTeamByName(teamName):
	return db.teams.find_one({"teamName": teamName})

def getTeamByEmail(email):
	return db.teams.find_one({"email": email})

def getTeamById(teamId):
	return db.teams.find_one({"_id": ObjectId(teamId)})

def getAdmin():
	return db.teams.find_one({"isAdmin": True})
