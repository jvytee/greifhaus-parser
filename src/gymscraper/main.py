import logging
from argparse import ArgumentParser

from .config import load_targets, generate_config, DEFAULT_TARGETS
from .scraper import scrape_targets


def main():
    message_format = "[%(levelname)s] %(asctime)s %(module)s:%(funcName)s - %(message)s"
    logging.basicConfig(format=message_format, level=logging.DEBUG)

    parser = ArgumentParser(description="Scrape gym visitor count")
    parser.add_argument("-c", "--config", type=str, default="config.toml", help="general configuration file", metavar="FILE")
    parser.add_argument("-t", "--target", type=str, default="target.toml", help="target configuration file", metavar="FILE")
    parser.add_argument("--generate-target-config", type=str, help="generate default target configuration", metavar="FILE")
    args = parser.parse_args()

    if args.generate_target_config is not None:
        logging.debug("Generating target configuration file %s", args.generate_target_config)
        generate_config(args.generate_target_config, DEFAULT_TARGETS)
        return

    targets = load_targets(args.target)
    logging.debug("Loaded targets: %s", targets)

    scrape_targets(targets)
