from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

client = MongoClient("localhost", 27017)
db = client.mteval

def addComp(compName, description, deadline, submissionFormat, requirements, organisers, contact, testData, trainingData):
	res = None
	comp = {
		"compName": compName,
		"description": description,
		"deadline": deadline,
		"format": submissionFormat, 
		"requirements": requirements,
		"organisers": organisers,
		"contact": contact, 
		"testData": testData,
		"trainingData": trainingData
	}

	db.competitions.insert_one(comp)
	res = {
		"success": True
	}
	return res

def editComp(oldName, newName, description, deadline, submissionFormat, requirements, organisers, contact, testData, trainingData):
	db.competitions.update(
	{"compName": oldName}, 
	{"$set": {
		"compName": newName,
		"description": description,
		"deadline": deadline,
		"format": submissionFormat, 
		"requirements": requirements,
		"organisers": organisers,
		"contact": contact, 
		"testData": testData,
		"trainingData": trainingData
	}})

def removeComp(compName):
	db.competitions.delete_one({"compName": compName})

def getCompByName(compName):
	return db.competitions.find_one({"compName": compName})

def getCompByEmail(email):
	return db.competitions.find_one({"email": email})

def getCompById(compId):
	return db.competitions.find_one({"_id": ObjectId(compId)})

def getCompList():
	comps = db.competitions.find()
	res = []
	for comp in comps:
		comp["_id"] = str(comp["_id"])
		res.append(comp)
	return res

def getUpcomingCompList():
	now = datetime.datetime.now()
	comps = db.competitions.find({"deadline": {"$gt": now}})
	res = []
	for comp in comps:
		comp["_id"] = str(comp["_id"])
		res.append(comp)
	return res

def getAdmin():
	return db.competitions.find_one({"isAdmin": True})

def acceptComp(compName):
	db.competitions.update({"compName": compName}, {"$set": {"isActive": True}})
