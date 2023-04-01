import argparse
import json
import os
import random

import numpy as np

IDEAS_FILENAME = "ideas.json"


class Date:
    def __init__(self, policy, ideas):
        self.policy = policy
        self.order = ["activity", "food", "dessert"]
        self.comp_type_to_list = {
            "activity": ideas["activities"],
            "food": ideas["foods"],
            "dessert": ideas["desserts"],
        }

    def generate(self):
        self.__randomize_comp_lists() #Generate random date each time
        date = self.__get_valid_date()
        # Print final result
        print(
            "Your next date:",
            ", ".join([date[piece]["name"] for piece in self.order]),
        )

    def __randomize_comp_lists(self):
        for comp_type, list in self.comp_type_to_list.items():
            self.comp_type_to_list[comp_type] = random.sample(list, len(list))

    def __get_valid_date(self):
        first_comp_type = self.order[0]
        to_explore = [
            (first_comp_type, p) for p in self.comp_type_to_list[first_comp_type]
        ]
        date = {}
        while len(to_explore) > 0:
            comp_type, comp = to_explore.pop()
            date[comp_type] = comp
            if self.policy.is_valid(**date):
                if len(date) == len(self.order):
                    return date
                next_comp_type = self.__get_next_comp_type(comp_type)
                to_explore.extend(
                    [(next_comp_type, p)
                     for p in self.comp_type_to_list[next_comp_type]
                     ]
                )
            else:
                del date[comp_type]
        raise Exception("Date cannot be generated with current constraints")

    def __get_next_comp_type(self, curr_comp_type):
        return self.order[self.order.index(curr_comp_type) + 1]

class DatePolicy:
    def __init__(self, activity_level, food_level, dessert_level, is_biking, required, ideas):
        self.activity_level, self.food_level, self.dessert_level, self.is_biking, self.required = (
            activity_level,
            food_level,
            dessert_level,
            is_biking,
            required
        )
        self.comp_type_to_list = {
            "activity": ideas["activities"],
            "food": ideas["foods"],
            "dessert": ideas["desserts"],
        }
        if self.required:
            self.required_comp_type = self.__get_comp_type_from_name(
                self.required
            )
        self.comp_type_to_comp = {}

    def is_valid(self, activity=None, food=None, dessert=None):
        #Determines if outfit satiesfies policy
        self.comp_type_to_comp = {
            "activity": activity,
            "food": food,
            "dessert": dessert,
        }
        if self.__meets_activity_level(activity)\
                and self.__meets_dessert_level(dessert)\
                and self.__meets_food_level(food)\
                and self.__is_biking(food, dessert):
            return True

    def __meets_activity_level(self, activity):
        if activity == None:
            return True
        if activity["attributes"]["active"] == self.activity_level:
            return True
        return None

    def __meets_food_level(self, food):
        if food == None or food["attributes"]["fancy"] == self.food_level:
            return True
        return None

    def __meets_dessert_level(self, dessert):
        if dessert == None or dessert["attributes"]["fancy"] == self.dessert_level:
            return True
        return None

    def __is_biking(self, food, dessert):
        if (food == None or food["attributes"]["biking"] == self.is_biking) \
                and (dessert == None or dessert["attributes"]["biking"] == self.is_biking):
            return True
        return None

    def __contains_required_comp_for_comp_type(self):
        for comp_type, comp in self.comp_type_to_comp.items():
            if (
                    comp and self.required_comp_type == comp_type
                    and comp["name"] != self.required
            ):
                return False
        return True

    def __get_comp_type_from_name(self, comp_name):
        for comp_type, comps in self.comp_type_to_list.items():
            if len(list(filter(lambda p: p["name"] == comp_name, comps))) > 0:
                return comp_type
        raise argparse.ArgumentTypeError(
            "Does not exist"
        )

def argsParser():
    #Activity parameters 1 to 3, food 1 to 5, desserts 1 to 3
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument("-a", "--active", type=int, required=False, choices=range(1,4))
    arg_parse.add_argument("-f", "--fancy", type=int, required=False, choices=range(1, 5))
    arg_parse.add_argument("-b", "--biking", action="store_true", help="if specificed, all pieces must be fancy")
    arg_parse.add_argument("-r", "--required", type=str)
    args = arg_parse.parse_args()
    return args

if __name__ == "__main__":
    args = argsParser()
    print("Your current parameters are:")
    print("Activity Strenuous Level:", args.active)
    print("Food Fanciness Level:", args.fancy)
    print("Dessert Fanciness Level:", args.fancy)
    print("Is it biking:", args.biking)
    print("Required component", args.required)
    ideas=None
    with open("ideas.json", "r") as f:
        ideas=json.load(f)
    # Create date policy
    policy = DatePolicy(args.active, args.fancy, args.fancy, args.biking, args.required, ideas)
    Date(policy, ideas).generate()
