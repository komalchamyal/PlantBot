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


# actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import sqlite3

class ActionGetPlantInfo(FormAction):
    def name(self) -> Text:
        return "action_get_plant_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        plant_name = tracker.get_slot('plant')
        
        conn = sqlite3.connect('plants.db')
        plant = conn.execute('SELECT * FROM plants WHERE name = ?', (plant_name,)).fetchone()
        conn.close()
        
        if plant:
            dispatcher.utter_message(text=f"Name: {plant['name']}\n"
                                          f"Scientific Name: {plant['scientific_name']}\n"
                                          f"Family: {plant['family']}\n"
                                          f"Description: {plant['description']}\n"
                                          f"Care Instructions: {plant['care_instructions']}")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find information about that plant.")
        
        return []
