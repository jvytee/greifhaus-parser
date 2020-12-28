import logging
import re
import urllib.request
from enum import Enum
from bs4 import BeautifulSoup


class Gym(Enum):
    BOULDERADO = "boulderado"
    WEBCLIMBER = "webclimber"
    ROCKGYMPRO = "rock-gym-pro"


def getClientCount(target):
    logging.debug("Getting client count for %s", target)

    url = target["url"]
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, features="lxml")

    if target["type"] == Gym.BOULDERADO:
        return parseBoulderado(soup)
    elif target["type"] == Gym.WEBCLIMBER:
        return parseWebclimber(soup)
    elif target["type"] == Gym.ROCKGYMPRO:
        return parseRockGymPro(soup, target["location"])


def parseBoulderado(soup):
    currentVisitors = None
    currentFree = None
    for div in soup.find_all("div"):
        if div["class"] == ["actcounter", "zoom"]:
            currentVisitors = div["data-value"]
        if div["class"] == ["freecounter", "zoom"]:
            currentFree = div["data-value"]
    return (currentVisitors, currentFree)


def parseWebclimber(soup):
    currentVisitors = None
    currentFree = None
    for div in soup.find_all("div"):
        if "style" in div.attrs:
            currentVisitors = int(re.search(r"width: (\d+?)%;", div["style"]).group(1))
            currentFree = 100 - currentVisitors
    return (currentVisitors, currentFree)


def parseRockGymPro(soup, location):
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
