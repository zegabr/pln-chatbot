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

api_url = "https://api.yelp.com/v3/businesses"
api_key = "xTB47wf9wc8u1C0MrGmkpK3Qx0Ah06BKFN8er8IT9FkaY31oD-rcPmb3VX8O8RSMP_f9cJt6UcOtcb_Sm8FK-XYhjovAKoqjX8wbfEFp5o58d5stlQkF-PmaXjoYYXYx"
api_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Authorization": f"Bearer {api_key}",
}


def make_search_request(params):
    try:
        response = requests.get(f"{api_url}/search",
                                headers=api_headers, params=params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    return response


def make_request_by_id(id):
    try:
        response = requests.get(f"{api_url}/{id}",
                                headers=api_headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    return response


class GetRestaurantPhoneNumber(Action):
    def name(self) -> Text:
        return "get_restaurant_phone_number"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        seenRestaurants = tracker.get_slot("seen_restaurants")
        restaurantId = seenRestaurants.split(",")[-1]

        if not restaurantId:
            dispatcher.utter_message(text="ERROR.")
            return []

        response = make_request_by_id(restaurantId)
        restaurant = response.json()

        if not restaurant:
            dispatcher.utter_message(
                text="Sorry, I couldn't find a restaurant :(")
            return []

        name = restaurant["name"]
        phone = restaurant["display_phone"]

        message = f"Here is the phone number for {name}: {phone}. Do you want to make a reservation?"
        dispatcher.utter_message(text=message)
        return []


class GetRestaurantAddress(Action):
    def name(self) -> Text:
        return "get_restaurant_address"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        seenRestaurants = tracker.get_slot("seen_restaurants")
        restaurantId = seenRestaurants.split(",")[-1]

        if not restaurantId:
            dispatcher.utter_message(text="ERROR.")
            return []

        response = make_request_by_id(restaurantId)
        restaurant = response.json()

        if not restaurant:
            dispatcher.utter_message(
                text="Sorry, I couldn't find a restaurant :(")
            return []

        name = restaurant["name"]
        address = restaurant["location"]["display_address"]
        addressString = ""
        for addressPart in address:
            addressString = addressString + addressPart + "\n"

        message = f"Here is the address for {name}:\n{addressString}\nDo you want to make a reservation?"
        dispatcher.utter_message(text=message)
        return []


class GetRestaurantsByParams(Action):
    def name(self) -> Text:
        return "get_restaurants_by_params"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        food = tracker.get_slot("cuisine")
        price = tracker.get_slot("price_range")
        reservationTime = tracker.get_slot("time")
        city = tracker.get_slot("city")

        params = {
            "location": "Recife"
        }

        if city:
            params["location"] = city
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

        response = make_search_request(params)
        restaurants = (json.loads(response.content))["businesses"]

        if not len(restaurants):
            dispatcher.utter_message(
                text="Sorry, I couldn't find any restaurants :(")
            return []

        seenRestaurants = tracker.get_slot("seen_restaurants") or ""
        restaurant = None
        for rest in restaurants:
            if rest["id"] not in seenRestaurants:
                restaurant = rest
                restId = rest["id"]
                seenRestaurants += f",{restId}"
                break

        if not restaurant:
            dispatcher.utter_message(
                text="Sorry, I couldn't find any more restaurants :(")
            return []

        restaurantName = restaurant["name"]

        dispatcher.utter_message(
            text=f"Here is the perfect restaurant for you! {restaurantName}. Do you want to make a reservation?")

        return [SlotSet("seen_restaurants", seenRestaurants), SlotSet("restaurant_name", restaurantName)]
