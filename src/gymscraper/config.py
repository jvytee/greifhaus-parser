import json
import logging
import os
from datetime import datetime

from .parser import Gym


defaultConfig = {
    "targets": [
        {
            "name": "greifhaus",
            "url": "https://www.boulderado.de/boulderadoweb/gym-clientcounter/index.php?mode=get&token=eyJhbGciOiJIUzI1NiIsICJ0eXAiOiJKV1QifQ.eyJjdXN0b21lciI6IkdyZWlmaGF1cyJ9.3Nen_IU5N2sVtJbP44CGCFfdKY93zQx2FRczY4z9Jy0",
            "type": Gym.BOULDERADO,
        },
        {
            "name": "fliegerhalle",
            "url": "https://158.webclimber.de/de/trafficlight?callback=WebclimberTrafficlight.insertTrafficlight&key=yspPh6Mr2KdST3br8WC7X8p6BdETgmPn&hid=158&container=trafficlightContainer&type=&area=",
            "type": Gym.WEBCLIMBER,
        },
        {
            "name": "the-spot-boulder",
            "url": "https://portal.rockgympro.com/portal/public/415a34a23151c6546419c1415d122b61/occupancy?&iframeid=occupancyCounter&fId=",
            "type": Gym.ROCKGYMPRO,
            "location": "BLD",
        },
        {
            "name": "the-spot-denver",
            "url": "https://portal.rockgympro.com/portal/public/415a34a23151c6546419c1415d122b61/occupancy?&iframeid=occupancyCounter&fId=",
            "type": Gym.ROCKGYMPRO,
            "location": "DEN",
        },
    ],
    "outputDir": os.path.dirname(__file__),
}


def loadConfig():
    # constants
    configDir = os.path.dirname(__file__)
    configFilename = os.path.join(configDir, "config.json")
    # check if file exists
    if not os.path.isfile(configFilename):
        logging.error('File "%s" not found. Creating empty config file, please fill in the empty fields', configFilename)
        createEmptyConfig(configFilename, defaultConfig)
        return None
    # try loading the config
    with open(configFilename, "r") as configFile:
        try:
            config = json.load(configFile)
        except json.decoder.JSONDecodeError:
            logging.error("Corrupt config. Creating empty config file, please fill in the empty fiels")
            createEmptyConfig(configFilename, defaultConfig)
            return None
    # check all fields exists
    for key in defaultConfig:
        if not key in config or type(defaultConfig[key]) is not type(config[key]):
            logging.error('File "mail.config" incomplete. %s is missing or invalid. Renaming old config file and generating new config', key)
            createEmptyConfig(configFilename, defaultConfig)
            return None
    # return valid config
    return config


def createEmptyConfig(filename, defaultConfig):
    saveOldConfig(filename)
    with open(filename, "w") as configFile:
        json.dump(defaultConfig, configFile)


def saveOldConfig(filename):
    if not os.path.exists(filename):
        return
    targetFileName = "{0}_{1}.json".format(
        os.path.splitext(filename)[0], getTimeForFilename()
    )
    if os.path.exists(targetFileName):
        os.remove(targetFileName)
    os.rename(filename, targetFileName)


def getTimeForFilename():
    return datetime.now().strftime("%Y-%m-%d-%H%M%S")