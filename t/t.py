import pathlib
from copy import deepcopy
from dataclasses import dataclass
from subprocess import Popen

import click
import requests_html
from keyboard import write as write_key
from requests.sessions import session
from termcolor import colored

from t.common import check_langs, check_platform
from t.extract import Parser

# WORKER, LANGS = check_langs()


@dataclass
class T:
    """
    docstring
    """

    nosay: bool = False
    lang: str = "english"
    sounds: str = "uk"
    current: str = "hello"
    worker: object = requests_html.HTMLSession()
    host = "dictionary.cambridge.org"
    voice_file = pathlib.Path("voice.mp3")
    platform = check_platform()

    def __post_init__(self):
        self.main_url = f"https://{self.host}"
        self.worker.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
            "AMP-Same-Origin": "true",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": self.main_url,
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        }

    def play_voice(self, url):
        body = self.worker.get(url).content
        with self.voice_file.open("wb") as file:
            file.write(body)
        Popen(self.platform["audio"].format(self.voice_file.absolute()), shell=True)

    def fetch_dictionary(self):
        resp = self.worker.get(
            f"{self.main_url}/search/direct/?datasetsearch={self.lang}&q={self.current}"
        )
        datas = Parser.dictionary(resp)
        datas["word"] = self.current
        self.print_words(datas)

    def associate_dictionary(self, words: str):
        resp = self.worker.get(
            f"{self.main_url}/autocomplete/amp?dataset={self.lang}&q={words}&__amp_source_origin={self.main_url}"
        )
        return Parser.associate(resp)

    def print_words(self, datas: dict):
        r = lambda _: colored(_, "red")
        c = lambda _: colored(_, "cyan")
        g = lambda _: colored(_, "green")
        b = lambda _: colored(_, "blue")
        y = lambda _: colored(_, "yellow")
        m = lambda _: colored(_, "magenta")
        """
        {
            "uk": {
                "mp3": "https://dictionary.cambridge.org/media/english/uk_pron/u/ukh/ukhef/ukheft_029.mp3",
                "pron": "heˈləʊ",
            },
            "us": {
                "mp3": "https://dictionary.cambridge.org/media/english/us_pron/h/hel/hello/hello.mp3",
                "pron": "heˈloʊ",
            },
        }
        """

        title = c(datas["word"].title())
        sounds = "   ".join(
            [
                f"""{y(region.upper()+'.')} {g(val['pron'])}"""
                for region, val in datas["sounds"].items()
            ]
        )

        words = f"""
{title}

{sounds}

{m(datas['meaning'].replace(':',''))}"""

        examples = "\r\n\r\n".join(map(lambda _: c(f"🌟  {_}"), datas["examples"][:3]))
        if examples.strip():
            words += f"\r\n\r\n\r\n{examples}"

        if not self.nosay:
            self.play_voice(datas["sounds"][self.sounds]["mp3"])
        print(words)

    def start(self):
        self.fetch_dictionary()


@click.command()
@click.option("-n", "--nosay", is_flag=True)
@click.option("-c", "--current", default="")
@click.option(
    "-l",
    "--sounds",
    type=click.Choice(["uk", "us"], case_sensitive=False),
    default="uk",
)
# @click.option("--lang", type=click.Choice(LANGS, case_sensitive=False))
def main(**kwargs):
    # T(worker=WORKER, **kwargs).start()
    T(**kwargs).start()


if __name__ == "__main__":
    main()
