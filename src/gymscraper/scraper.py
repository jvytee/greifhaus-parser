import logging
import os
from datetime import datetime

from .parser import getClientCount


def parseTarget(target, outputDir):
    logging.debug("Parsing target %s", target)

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