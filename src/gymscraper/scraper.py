import httpx
import logging
from bs4 import BeautifulSoup
from typing import Callable, List, Optional, Tuple

from . import parser
from .config import Target


def scrape_targets(targets: List[Target]):
    logging.debug("Scraping targets")

    for target in targets:
        parser_function = parser.get_parser(target.gym_type)

        visitors, free = scrape(target.url, parser_function, target.location)
        save(target.name, visitors, free)


def scrape(url: str, parser_function: Callable, location: Optional[str] = None) -> Tuple[int, int]:
    logging.debug("Scraping %s", url)

    response = httpx.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="lxml")

    if location is None:
        visitors, free = parser_function(soup)
    else:
        visitors, free = parser_function(soup, location)

    return (visitors, free)


def save(name: str, visitors: int, free: int):
    logging.debug("%s: %s visitors, %s free", name, visitors, free)
