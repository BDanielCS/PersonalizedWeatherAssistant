# users.py

"""
Handles the data regarding the preferences for
individual users. Users preferences focus on
their current location for weather
to be displayed and other basic user profile
features

"""

import boto3
import secure_hash
import preferences


class User:
	"""	
	Represents a user within our system. Each user 
	object is stored within the db
	"""

	def __init__(self):
		self.name = None
		self.city = None
		self.state = None
		self.userID = -1

	def __init__(self, name, state, city):
		self.name = name
		self.city = city
		self.state = state
		self.userID = secure_hash.totalHash(name, city)
		 

def getUserProfile(name, city):
	"""
	Grab user preferences from the dynamodb database
	and return as User instance.  If no entry exists, then
	return -1

	"""

	client = boto3.client('dynamodb')
	response = client.get_item(
		TableName='UserPreferences',
		Key={
			'UserID':{
				'S': secure_hash.totalHash(name, city)
			}
		}
	)

	return response


def saveUserProfile(user):
	"""
	Given a user object, save that user within
	the dynamodb 
	"""

	client = boto3.client('dynamodb')
	response = client.put_item(
		TableName='UserPreferences',
		Item={
			'UserID': {
				'S': user.userID
				},
			'Name': {
				'S': user.name,
				},
			'State': {
				'S': user.state
				},
			'City': {
				'S':user.city
			}
		}
	)

	return response


def deleteUserProfile(user):
	"""
	Given the user object, delete the preferences 
	blob from the db
	"""

	client = boto3.client('dynamodb')
	response = client.delete_item(
		TableName='UserPreferences',
		Key={
			'UserID':{
				'S': secure_hash.totalHash(user.name, user.city)
			}
		}
	)

	return response
	
