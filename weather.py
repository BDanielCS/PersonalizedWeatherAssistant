# weather.py

import requests
import json

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

	