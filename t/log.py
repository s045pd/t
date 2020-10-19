import logging

from termcolor import colored

logging.basicConfig(format="%(message)s", level=logging.INFO)
loger = logging.getLogger("")


def info(txt: str) -> None:
    loger.info("[+]{}".format(colored(txt, "blue")))


def success(txt: str) -> None:
    loger.info("[*]{}".format(colored(txt, "green")))


def warning(txt: str) -> None:
    loger.warning("[=]{}".format(colored(txt, "yellow")))


def error(txt: str) -> None:
    loger.error("[-]{}".format(colored(txt, "red")))


def critical(txt: str) -> None:
    loger.error("[x]{}".format(colored(txt, "red")))
