# Date Night Planner
This is a Python command-line application that helps you plan your next date night. It generates a random date that satisfies your preferences and requirements for activity, food, and dessert.

## Installation
Clone the repository.
Install the required packages: numpy.
Create an ideas.json file in the root directory. This file should contain a list of activities, foods, and desserts. The attached json file is an example of what it could look like. 

## Usage
To run the program, use the following command:
python date_planner.py [-h] [-a ACTIVE] [-f FANCY] [-b] [-r REQUIRED]

Here are the available options:

-h, --help: show the help message and exit
-a ACTIVE: set the strenuous level for the activity (1-3)
-f FANCY: set the fanciness level for the food and dessert (1-5)
-b: set whether the date should involve biking
-r REQUIRED: set the required component (activity, food, or dessert)
The program will generate a random date that satisfies your preferences and requirements. If no valid date can be generated with the given constraints, the program will raise an exception.
