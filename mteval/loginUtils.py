from flask import Flask, request
from flask.ext import login
from werkzeug.security import generate_password_hash, check_password_hash
from database import teamDB

class Team(object):

	def __init__(self, teamId, 
					isAdmin, teamName, email, passwordHash, emailVerified):
		self.teamId 		= teamId
		self.isAdmin 		= isAdmin
		self.teamName		= teamName
		self.email			= email
		self.passwordHash	= passwordHash
		self.emailVerified  = emailVerified

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.teamId

	def is_verified(self):
		return self.emailVerified	


# #returns a Team object if valid userId, None otherwise
# def getTeamObject(userId):
# 	#get the database function
# 	isPendingUser = False
# 	user = teamDB.getUserById(userId)
# 	if user == None or user == {}:
# 		return None

# 	return User(userId, user.get('isApproved'), user.get('isAdmin'), 
# 				user['username'], user['email'], user['passwordHash'], 
# 				user.get('apiKey'), user.get('emailVerified'))


#userStringId can be username or email 
#returns a status
def loginUser(userStringId, password):
	status = {
		'isValid': False,
		'reason': ''
	}
	#check if valid userName/email
	team = teamDB.getTeamByName(userStringId)
	if team == None:
		team = teamDB.getTeamByEmail(userStringId)
	if team == None:
		status['reason'] = 'Error: Invalid username/email address'
		return status
	
	print team

	team = Team(str(team.get("_id")), team.get('isAdmin'), 
				team['teamName'], team['email'], team['passwordHash'], 
				team.get('emailVerified'))
	
	# if not team.is_active():
	# 	status['reason'] = 'Error: You registration has not been accepted yet.'
	# 	return status

	# if not team.is_verified():
	# 	status['reason'] = 'Error: Email not verified'	
	# 	return status

	if not checkTeamPassword(team, password):
		status['reason'] = 'Error: Wrong password.'
		return status

	#actually log in the user
	login.login_user(team)

	status['isValid'] = True

	return status

def hashPassword(password):
	return generate_password_hash(password)

def checkTeamPassword(teamObj, passwordStr):
	return  check_password_hash(teamObj.passwordHash, passwordStr)