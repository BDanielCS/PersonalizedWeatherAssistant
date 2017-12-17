# preferences.py

"""
Container for clothing preferences.
contains all the the user's current preferences
and updates based on agreement with the aws ml
model. When the model is incorrect, store current conditions
in the weather history db with the user's preferred choice
of layers.
"""

import boto3
import math
import json


def predict(user, passw, weather_features):
	"""
	Invoke the aws ml model to offer a 
	prediction for the number of layers to
	be wearing today. Also check if a previously 
	stored prediction was made.  If a prediction was stored,
	then use the stored prediction instead of model
	prediction
	@rType: int
	"""
	ml_client = boto3.client('machinelearning')
	db_client = boto3.client('dynamodb')

	# check to see if this user has any applicable stored predictions
	get_response = db_client.get_item(
		TableName='WeatherDecision',
		Key={
			'userID':{
				'S':total_hash(user,passw)
			},
			'Temperature':{
				'N':str(math.floor(weather_features['raw_temp']))
			}
		}
	)

	# if we got a match, return the previous setting instead
	if len(get_response) >= 2:
		return int(get_response['Item']['Subconditions']['M']['Layers']['N'])


	# perform a prediction using the model
	weather_conditions = {
		'UserID':userID,
		'Temperature': str(math.floor(weather_features['raw_temp'])),
		'WindSpeed': str(weather_features['max wind speed']),
		'Raining': '1' if int(weather_features['chance of rain']) > 50 else '0', 
		'Snowing': '1' if int(weather_features['snow']) > 1 else '0',
		'Cloudy': '1' if weather_features['general forcast'] == 'Cloudy' else '0'
	}

	response = ml_client.predict(
		MLModelId='ml-RgLcS6do8rZ',
		Record=weather_conditions,
		PredictEndpoint='https://realtime.machinelearning.us-east-1.amazonaws.com'
	)

	num_layers = math.ceil(response['Prediction']['predictedValue'])
	return num_layers, weather_conditions


def updatePrediction(UID, desired_layers, weather_conditions):
	"""
	Save the current weather features with the user's desired
	number of layers into the dynamodb.  Weather conditions is expected
	to be on the form which predict() outputs
	"""

	client = boto3.client('dynamodb')
	weather_conditions['Layers'] = desired_layers

	response = client.put_item(
		TableName='WeatherDecision',
		Item={
			'userID':{
				'S': UID
			},
			'Temperature':{
				'N': weather_conditions['Temperature']
			},
			'Subconditions':{
				'M': {
					'Layers':{
						'N':str(desired_layers)
					},
					'WindSpeed':{
						'N': weather_conditions['WindSpeed']
					},
					'Raining':{
						'N': weather_conditions['Raining']
					},
					'Snowing':{
						'N': weather_conditions['Snowing']
					},
					'Cloudy':{
						'N': weather_conditions['Cloudy']
					}
				}
			}
		}
	)

	return response
