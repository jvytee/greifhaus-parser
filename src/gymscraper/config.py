import json
import logging
import os
from datetime import datetime
from typing import Optional

from .parser import Gym


defaultConfig = {
    "targets": [
        {
            "name": "greifhaus",
            "url": "https://www.boulderado.de/boulderadoweb/gym-clientcounter/index.php?mode=get&token=eyJhbGciOiJIUzI1NiIsICJ0eXAiOiJKV1QifQ.eyJjdXN0b21lciI6IkdyZWlmaGF1cyJ9.3Nen_IU5N2sVtJbP44CGCFfdKY93zQx2FRczY4z9Jy0",
            "type": Gym.BOULDERADO.value,
        },
        {
            "name": "fliegerhalle",
            "url": "https://158.webclimber.de/de/trafficlight?callback=WebclimberTrafficlight.insertTrafficlight&key=yspPh6Mr2KdST3br8WC7X8p6BdETgmPn&hid=158&container=trafficlightContainer&type=&area=",
            "type": Gym.WEBCLIMBER.value,
        },
        {
            "name": "the-spot-boulder",
            "url": "https://portal.rockgympro.com/portal/public/415a34a23151c6546419c1415d122b61/occupancy?&iframeid=occupancyCounter&fId=",
            "type": Gym.ROCKGYMPRO.value,
            "location": "BLD",
        },
        {
            "name": "the-spot-denver",
            "url": "https://portal.rockgympro.com/portal/public/415a34a23151c6546419c1415d122b61/occupancy?&iframeid=occupancyCounter&fId=",
            "type": Gym.ROCKGYMPRO.value,
            "location": "DEN",
        },
    ],
    "outputDir": os.path.dirname(__file__),
}


# def loadConfig(filename: str) -> Optional[dict]:
#     # check if file exists
#     if not os.path.isfile(filename):
#         logging.error('File "%s" not found. Creating empty config file, please fill in the empty fields', filename)
#         createEmptyConfig(filename, defaultConfig)
#         return None
# 
#     # try loading the config
#     with open(filename, "r") as configFile:
#         try:
#             config = json.load(configFile)
#         except json.decoder.JSONDecodeError:
#             logging.error("Corrupt config. Creating empty config file, please fill in the empty fiels")
#             createEmptyConfig(filename, defaultConfig)
#             return None
# 
#     # check all fields exists
#     for key in defaultConfig:
#         if not key in config or type(defaultConfig[key]) is not type(config[key]):
#             logging.error('File "mail.config" incomplete. %s is missing or invalid. Renaming old config file and generating new config', key)
#             createEmptyConfig(filename, defaultConfig)
#             return None
# 
#     # return valid config
#     return config
# 
# 
# def createEmptyConfig(filename: str, defaultConfig: dict):
#     saveOldConfig(filename)
# 
#     with open(filename, "w") as configFile:
#         json.dump(defaultConfig, configFile)
# 
# 
# def saveOldConfig(filename: str):
#     if not os.path.exists(filename):
#         return
# 
#     targetFileName = "{0}_{1}.json".format(
#         os.path.splitext(filename)[0], getTimeForFilename()
#     )
# 
#     if os.path.exists(targetFileName):
#         os.remove(targetFileName)
# 
#     os.rename(filename, targetFileName)
# 
# 
# def getTimeForFilename():
#     return datetime.now().strftime("%Y-%m-%d-%H%M%S")


def load_config(filename: str) -> Optional[dict]:
    try:
        with open(filename, "r") as f:
            config = json.load(f)
            return config
    except FileNotFoundError as e:
        logging.error("File %s not found: %s", filename, e)
    except json.decoder.JSONDecodeError as e:
        logging.error("Could not load JSON: %s", e)

    return None


def generate_config(filename: str, config: dict):
    with open(filename, "w") as f:
        json.dump(config, f)


def verify_config(config: dict):
    return all(key in config and isinstance(defaultConfig[key], type(value)) for key, value in defaultConfig.items())
