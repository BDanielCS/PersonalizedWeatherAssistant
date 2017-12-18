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
import hashlib
import requests


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


def _get_weather(f_type, state, city):
	"""
	Making the call to the wunderground api to grab forecast
	for specified location within the USA
	@param forecast_type:
	@param state:
	@param city:
	@rType: dict
	"""
	
	request = ('http://api.wunderground.com/api/61ef2eec71888acb/' + str(f_type)
		+ '/q/' + str(state) + '/' + str(city) + '.json')

	r = requests.get(request)
	return r.json()


def getCurrentWeather(state, city):
	"""
	Grab the current weather status 
	from the wundergroup request. Extract the necessary
	features to be displayed. Return dictionary
	of weather features
	"""

	weather_features = dict()
	raw_weather = _get_weather('conditions', state, city)
	raw_forecast = _get_weather('forecast', state, city)
	raw_current_forcast = raw_forecast['forecast']['txt_forecast']['forecastday']
	simple_forcast = raw_forecast['forecast']['simpleforecast']['forecastday']

	# extracting essential features
	weather_features['temp'] = \
		raw_weather['current_observation']['temperature_string']
	weather_features['raw_temp'] = \
		raw_weather['current_observation']['temp_f']
	weather_features['observation time'] = \
		raw_weather['current_observation']['observation_time']
	weather_features['general forcast'] = \
		raw_weather['current_observation']['weather']
	weather_features['general forcast picture'] =\
		raw_current_forcast[0]['icon_url']
	weather_features['general forcast description'] =\
		raw_current_forcast[0]['fcttext']
	weather_features['chance of rain'] =\
		raw_current_forcast[0]['pop']
	weather_features['humidity'] = \
		raw_weather['current_observation']['relative_humidity']
	weather_features['max wind speed'] = \
		raw_weather['current_observation']['wind_gust_mph']
	weather_features['feels like'] = \
		raw_weather['current_observation']['feelslike_string']
	weather_features['snow'] = \
		simple_forcast[0]['snow_allday']['in']

	return weather_features


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
	userID = total_hash(user,passw)

	# check to see if this user has any applicable stored predictions
	get_response = db_client.get_item(
		TableName='WeatherDecision',
		Key={
			'userID':{
				'S': userID
			},
			'Temperature':{
				'N':str(math.floor(weather_features['raw_temp']))
			}
		}
	)

	# perform a prediction using th
	weather_conditions = {
		'UserID':userID,
		'Temperature': str(math.floor(weather_features['raw_temp'])),
		'WindSpeed': str(weather_features['max wind speed']),
		'Raining': '1' if int(weather_features['chance of rain']) > 50 else '0', 
		'Snowing': '1' if int(weather_features['snow']) > 1 else '0',
		'Cloudy': '1' if weather_features['general forcast'] == 'Cloudy' else '0'
	}

	# if we got a match, return the previous setting instead
	if len(get_response) >= 2:
		return int(get_response['Item']['Subconditions']['M']['Layers']['N']), weather_conditions

	response = ml_client.predict(
		MLModelId='ml-RgLcS6do8rZ',
		Record=weather_conditions,
		PredictEndpoint='https://realtime.machinelearning.us-east-1.amazonaws.com'
	)

	num_layers = math.ceil(response['Prediction']['predictedValue'])
	return num_layers, weather_conditions


def updatePrediction(user,passw,desired_layers, weather_conditions):
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
				'S': total_hash(user,passw)
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


def layer_handler(event, context):
	user = event['Username']
	passw = event['Password']
	state = event['State']
	city = event['City']
	layers = event['Layers']

	weather_features = weather.getCurrentWeather(state, city)
	_, conditions = predict(user ,passw, weather_features)
	response = updatePrediction(user, passw, layers, conditions)
	
	return response
