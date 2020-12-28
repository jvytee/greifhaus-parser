import logging
from argparse import ArgumentParser

from .config import loadConfig
from .scraper import parseTarget


def main():
    message_format = "[%(levelname)s] %(asctime)s %(module)s:%(funcName)s - %(message)s"
    logging.basicConfig(format=message_format, level=logging.DEBUG)

    parser = ArgumentParser(description="Scrape gym visitor count")
    parser.add_argument("-c", "--config", type=str, default="config.json", help="configuration file", metavar="FILE")
    args = parser.parse_args()

    config = loadConfig(args.config)
    if not config:
        return

    outputDir = config["outputDir"]
    targets = config["targets"]

    for target in targets:
        parseTarget(target, outputDir)
