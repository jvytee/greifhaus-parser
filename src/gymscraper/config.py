import json
import logging
import os
from typing import Optional

from .parser import Gym


DEFAULT = {
    "targets": [
        {
            "name": "greifhaus",
            "url": "https://www.boulderado.de/boulderadoweb/gym-clientcounter/index.php?mode=get&token=eyJhbGciOiJIUzI1NiIsICJ0eXAiOiJKV1QifQ.eyJjdXN0b21lciI6IkdyZWlmaGF1cyJ9.3Nen_IU5N2sVtJbP44CGCFfdKY93zQx2FRczY4z9Jy0",
            "type": Gym.BOULDERADO.value,
        },
        {
            "name": "fliegerhalle",
            "url": "https://158.webclimber.de/de/trafficlight?callback=WebclimberTrafficlight.insertTrafficlight&key=yspPh6Mr2KdST3br8WC7X8p6BdETgmPn&hid=158&container=trafficlightContainer&type=&area=",
            "type": Gym.WEBCLIMBER.value,
        },
        {
            "name": "the-spot-boulder",
            "url": "https://portal.rockgympro.com/portal/public/415a34a23151c6546419c1415d122b61/occupancy?&iframeid=occupancyCounter&fId=",
            "type": Gym.ROCKGYMPRO.value,
            "location": "BLD",
        },
        {
            "name": "the-spot-denver",
            "url": "https://portal.rockgympro.com/portal/public/415a34a23151c6546419c1415d122b61/occupancy?&iframeid=occupancyCounter&fId=",
            "type": Gym.ROCKGYMPRO.value,
            "location": "DEN",
        },
    ],
    "outputDir": os.path.dirname(__file__),
}


def load_config(filename: str) -> Optional[dict]:
    try:
        with open(filename, "r") as f:
            config = json.load(f)
            return config
    except FileNotFoundError:
        logging.error("Configuration file %s not found", filename)
    except json.decoder.JSONDecodeError as e:
        logging.error("Could not decode JSON: %s", e)

    return None


def generate_config(filename: str, config: dict):
    with open(filename, "w") as f:
        json.dump(config, f)


def verify_config(config: dict) -> list:
    return [key for key, value in DEFAULT.items() if not (key in config and isinstance(config[key], type(value)))]
