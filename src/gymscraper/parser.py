import logging
import re
from enum import Enum


class Gym(Enum):
    BOULDERADO = "boulderado"
    WEBCLIMBER = "webclimber"
    ROCKGYMPRO = "rock-gym-pro"


def parseBoulderado(soup):
    logging.debug("Parsing boulderado")

    currentVisitors = None
    currentFree = None
    for div in soup.find_all("div"):
        if div["class"] == ["actcounter", "zoom"]:
            currentVisitors = div["data-value"]
        if div["class"] == ["freecounter", "zoom"]:
            currentFree = div["data-value"]
    return (currentVisitors, currentFree)


def parseWebclimber(soup):
    logging.debug("Parsing webclimber")

    currentVisitors = None
    currentFree = None
    for div in soup.find_all("div"):
        if "style" in div.attrs:
            currentVisitors = int(re.search(r"width: (\d+?)%;", div["style"]).group(1))
            currentFree = 100 - currentVisitors
    return (currentVisitors, currentFree)


def parseRockGymPro(soup, location):
    logging.debug("Parsing rockgympro")

    currentVisitors = None
    currentFree = None
    for script in soup.find_all("script"):
        contents = script.contents
        if contents and "capacity" in contents[0] and "count" in contents[0]:
            script = contents[0].replace("\n", "").replace(" ", "")
            filteredScript = re.search(rf"\'{location}\':{{(.+?)}}", script).group(1)
            capacity = int(re.search(r"\'capacity\':(\d+?),", filteredScript).group(1))
            currentVisitors = int(
                re.search(r"\'count\':(\d+?),", filteredScript).group(1)
            )
            currentFree = capacity - currentVisitors
    return (currentVisitors, currentFree)
