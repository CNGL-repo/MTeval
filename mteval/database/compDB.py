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
		"organiser": organisers,
		"contact": contact, 
		"testData": testData,
		"trainingData": trainingData
	}

	db.competitions.insert_one(comp)
	res = {
		"success": True
	}
	return res

def editComp(compName, description, deadline, submissionFormat, requirements, organisers, contact, testData, trainingData):
	db.competitions.update(
	{"compName": compName}, 
	{"$set": {
		"compName": compName,
		"description": description,
		"deadline": deadline,
		"format": submissionFormat, 
		"requirements": requirements,
		"organiser": organisers,
		"contact": contact, 
		"testData": testData,
		"trainingData": trainingData
	}})

def removeComp(compName):
	db.competitions.delete_one({"compName": compName})

def getCompByName(compName):
	return db.comps.find_one({"compName": compName})

def getCompByEmail(email):
	return db.comps.find_one({"email": email})

def getCompById(compId):
	return db.comps.find_one({"_id": ObjectId(compId)})

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
