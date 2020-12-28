import logging

from .config import loadConfig
from .scraper import parseTarget


def main():
    message_format = "[%(levelname)s] %(asctime)s %(module)s:%(funcName)s - %(message)s"
    logging.basicConfig(format=message_format, level=logging.DEBUG)
    config = loadConfig()

    if not config:
        exit(-1)

    outputDir = config["outputDir"]
    targets = config["targets"]

    for target in targets:
        parseTarget(target, outputDir)
