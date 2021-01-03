import logging
from argparse import ArgumentParser

from .config import load_targets, generate_config, DEFAULT
from .scraper import scrape_targets


def main():
    message_format = "[%(levelname)s] %(asctime)s %(module)s:%(funcName)s - %(message)s"
    logging.basicConfig(format=message_format, level=logging.DEBUG)

    parser = ArgumentParser(description="Scrape gym visitor count")
    parser.add_argument("-c", "--config", type=str, default="config.toml", help="general configuration file", metavar="FILE")
    parser.add_argument("-t", "--target", type=str, default="target.toml", help="target configuration file", metavar="FILE")
    parser.add_argument("--generate-config", type=str, help="generate default configuration file", metavar="FILE")
    args = parser.parse_args()

    if args.generate_config is not None:
        logging.debug("Generating configuration file %s", args.generate_config)
        generate_config(args.generate_config, DEFAULT)
        return

    # config = load_config(args.config)
    # if config is None:
    #     logging.error("Could not load configuration file %s", args.config)
    #     return

    # invalid_keys = verify_config(config)
    # if len(invalid_keys) > 0:
    #     logging.error("Missing or invalid keys: %s", invalid_keys)
    #     return

    # outputDir = config["outputDir"]
    # targets = config["targets"]

    targets = load_targets(args.target)
    logging.debug("Loaded targets: %s", targets)

    scrape_targets(targets)
