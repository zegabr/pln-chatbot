# actions/actions.py
from typing import Text, List, Optional, Dict, Any
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker, Action
from rasa_sdk.events import SlotSet
import os
import requests
import json
import uuid
import json
from datetime import date, datetime, timezone
import time

api_url = "https://api.yelp.com/v3/businesses/search"
api_key = "xTB47wf9wc8u1C0MrGmkpK3Qx0Ah06BKFN8er8IT9FkaY31oD-rcPmb3VX8O8RSMP_f9cJt6UcOtcb_Sm8FK-XYhjovAKoqjX8wbfEFp5o58d5stlQkF-PmaXjoYYXYx"
api_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Authorization": f"Bearer {api_key}",
}


def make_request(params):
    try:
        response = requests.get(api_url, headers=api_headers, params=params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    return response


class GetRestaurantInfo(Action):
    def name(self) -> Text:
        return "get_restaurant_info"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        restaurant = tracker.get_slot("restaurant_name")

        if not restaurant:
            dispatcher.utter_message(text="ERROR.")
            return []

        params = {
            "location": "recife",
            "term": restaurant
        }

        response = make_request(params)
        restaurants = (json.loads(response.content))["businesses"]

        if not len(restaurants):
            dispatcher.utter_message(
                text="Sorry, I couldn't find a restaurant with this name :(")
            return []

        restaurant = restaurants[0]
        print(restaurant)

        name = restaurant["name"]
        rating = restaurant["rating"]
        phone = restaurant["display_phone"]
        address = restaurant["location"]["display_address"]

        message = f"Here is some info about {name}:\n It has a rating of {rating} out of 5 stars.\n Its phone number is {phone}. And it is located at {address}."
        dispatcher.utter_message(text=message)
        return [SlotSet("restaurant_name", name)]


class GetRestaurantsByParams(Action):
    def name(self) -> Text:
        return "get_restaurants_by_params"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        food = tracker.get_slot("cuisine")
        price = tracker.get_slot("price_range")
        reservationTime = tracker.get_slot("time")

        params = {
            "location": "recife"
        }
        if food:
            params["term"] = food
        if price:
            if price == "inexpensive":
                params["price"] = "1"
            elif price == "moderate":
                params["price"] = "1,2"
            elif price == "moderate":
                params["price"] = "1,2,3"
            else:
                params["price"] = "1,2,3,4"
        if reservationTime:
            [hour, minutes] = reservationTime.split(":")
            today = date.today()
            goTime = datetime(today.year, today.month,
                              today.day, int(hour), int(minutes))
            unixTime = time.mktime(goTime.timetuple())
            params["open_at"] = int(unixTime)

        response = make_request(params)
        restaurants = (json.loads(response.content))["businesses"]

        if not len(restaurants):
            dispatcher.utter_message(
                text="Sorry, I couldn't find any restaurants :(")
            return []

        restaurantName = restaurants[0]["name"]

        dispatcher.utter_message(
            text=f"Here is the perfect restaurant for you! {restaurantName}.")

        return [SlotSet("suggested_restaurant", restaurantName)]
