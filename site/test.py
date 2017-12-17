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


def lambda_handler(event, context):
 """
	AWS Lambda handler for to create
	user within database
	"""
	field1 = event['Username']
	field2 = event['Password']

	response = createUser(field1, field2)

	return {'Response':response}
