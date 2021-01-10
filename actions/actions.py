# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

weather_dict = {'freezing_rain_heavy': 'Heavy rain and snow', 'freezing_rain': 'Rain and snow outside the house', 'freezing_rain_light': 'Light rain and snow', 'freezing_drizzle': 'Light drizzle and snow', 'ice_pellets_heavy': 'Heavy ice pellets falling form the sky.', 'ice_pellets': 'Ice pellets falling from the sky.', 'ice_pellets_light': 'Light pellets falling from the sky.', 'snow_heavy': 'Heavy snow around the area.', 'snow': 'It is snowing outside.', 'snow_light': 'Light snow around the area.', 'flurries': 'Flurries', 'tstorm': 'Thunder storm around the area.', 'rain_heavy': 'Heavy rain around the area.', 'rain': 'It is raining outside.', 'rain_light': 'Light rain around the area.', 'drizzle': 'It is drizzling outside.', 'fog_light': 'Light fog around the area.', 'fog': 'Presence of fog around the area.', 'cloudy': 'It is cloudly outside.', 'mostly_cloudy': 'The sky is covered with clouds.', 'partly_cloudy': 'It is partly cloudly outside', 'mostly_clear': 'Sunny with presence of small clouds.', 'clear': 'It is clear and sunny outside.'}
url = "https://api.climacell.co/v3/weather/realtime"

querystring = {"lat":"6.028849","lon":"80.785576","unit_system":"si","fields":"temp,humidity,weather_code","apikey":"xxxx"}

class ActionAskWeather(Action):
    def name(self) -> Text:
        return "action_ask_weather"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.request("GET", url, params=querystring)
        result = ""

        json_data = response.json()
        if(json_data['weather_code']['value'] in weather_dict):
            result = weather_dict[json_data['weather_code']['value']] + ' '

        result += 'Average temperature is %s%s while the humidity is about %s%s.' % (json_data['temp']['value'], json_data['temp']['units'], json_data['humidity']['value'], json_data['humidity']['units'])

        dispatcher.utter_message(text=result)

        return []