import logging
from argparse import ArgumentParser

from .config import load_config, generate_config, verify_config, DEFAULT
from .scraper import parseTarget


def main():
    message_format = "[%(levelname)s] %(asctime)s %(module)s:%(funcName)s - %(message)s"
    logging.basicConfig(format=message_format, level=logging.DEBUG)

    parser = ArgumentParser(description="Scrape gym visitor count")
    parser.add_argument("-c", "--config", type=str, default="config.json", help="configuration file", metavar="FILE")
    parser.add_argument("--generate-config", type=str, help="generate default configuration file", metavar="FILE")
    args = parser.parse_args()

    if args.generate_config is not None:
        logging.debug("Generating configuration file %s", args.generate_config)
        generate_config(args.generate_config, DEFAULT)
        return

    config = load_config(args.config)
    if config is None:
        logging.error("Could not load configuration file %s", args.config)
        return

    invalid_keys = verify_config(config)
    if len(invalid_keys) > 0:
        logging.error("Missing or invalid keys: %s", invalid_keys)
        return

    outputDir = config["outputDir"]
    targets = config["targets"]

    for target in targets:
        parseTarget(target, outputDir)
