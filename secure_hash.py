# secure_hash.py

"""
This modules handles the authentication and 
the creation / deletion of users
within the dynamodb. All fields are
encrypted with private keys depending on the
type of hash function used

"""

import hashlib
import boto3
import random
import string


def totalHash(field1, field2):
	"""
	Larger hash
	"""
	return hashlib.sha256(
		(simpleHash(field1)+simpleHash(field2)+simpleHash('state')) \
		.encode('utf-8')).hexdigest()


def simpleHash(field):
	"""
	Simple one field hash
	"""
	return hashlib.sha256((field).encode('utf-8')).hexdigest()


def authenticate(field1, field2):
	"""
	Prompted a username and password, ensure that
	the user has made an account and the  login information
	is correct
	"""
	salt = ['3.2..400zx','34ff4ff']
	client = boto3.client('dynamodb')
	response = client.get_item(
		TableName='userFields',
		Key={
			'Key':{
				'S':totalHash(field1, (salt[0] + field2))
			}
		}
	)

	return response


def createUser(field1, field2):
	"""
	Create a new user and add it to the
	usersdb
	"""

	salt = ['3.2..400zx','34ff4ff']
	client = boto3.client('dynamodb')
	response = client.put_item(
		TableName='userFields',
		Item={
			'Key':{
				'S':totalHash(field1, (salt[0]+ field2))
			},
			'Username':{
				'S': totalHash(field1, salt[1])
			},
			'Password':{
				'S': ''.join(random.choices(string.ascii_uppercase +
				 string.digits, k=25))
			}
		}
	)

	return response


def deleteUser(field1, field2):
	"""
	Delete the user from the db
	"""

	salt = '3.2..400zx'
	client = boto3.client('dynamodb')
	response = client.delete_item(
		TableName='userFields',
		Key={
			'Key':{
				'S': totalHash(field1, (salt + field2))
			}
		}
	)

	return response


def createUser_hander(event, context):
	"""
	AWS Lambda handler for to create
	user within database
	"""
	field1 = event['field1']
	field2 = event['field2']

	createUser(field1, field2)
	