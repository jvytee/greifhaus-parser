#!/usr/bin/python3

import json
import logging
import os
from datetime import datetime
from .parser import Gym, getClientCount

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


def parseTarget(target, outputDir):
    currentVisitors, currentFree = getClientCount(target)
    if currentVisitors is None or currentFree is None:
        logging.error("Failed to parse: currentVisitors = %s, currentFree = %s", currentVisitors, currentFree)
        exit(-1)

    counterFile = os.path.join(outputDir, "{}-counter.csv".format(target["name"]))
    latestDataFile = os.path.join(outputDir, "{}-latest.csv".format(target["name"]))
    csvExists = os.path.exists(counterFile)
    lastEntry = None
    currentTime = datetime.now().replace(microsecond=0).isoformat()
    newEntry = "{},{},{}\n".format(currentTime, currentVisitors, currentFree)

    if csvExists:
        with open(counterFile, "r") as outputCSV:
            for line in outputCSV:
                pass
            lastEntry = line

    with open(counterFile, "a") as outputCSV:
        if not csvExists:
            outputCSV.write("time,visitors,available\n")
        if (
            not lastEntry
            or not lastEntry.partition(",")[2] == newEntry.partition(",")[2]
        ):
            outputCSV.write(newEntry)

    with open(latestDataFile, "w") as latestDataCSV:
        latestDataCSV.write("time,visitors,available\n")
        latestDataCSV.write(newEntry)


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


# def getLogTime():
#     return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# 
# 
# class Log:
#     error = "ERROR"
#     info = "INFO"
#     debug = "DEBUG"
# 
#     @staticmethod
#     def log(tag, message):
#         print(
#             "[{time}] [{tag}] {message}".format(
#                 time=getLogTime(), tag=tag, message=message
#             )
#         )
