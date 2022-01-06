import sys
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile

import click
import requests_html
from playsound import playsound
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion, WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style

from termcolor import colored

from t.common import check_langs, check_platform
from t.extract import Parser

# WORKER, LANGS = check_langs()


BASE_DIR = Path(__file__).resolve().parent.parent


style = Style.from_dict(
    {
        "completion-menu.completion": "bg:#008888 #ffffff",
        "completion-menu.completion.current": "bg:#00aaaa #000000",
        "scrollbar.background": "bg:#88aaaa",
        "scrollbar.button": "bg:#222222",
    }
)


class CustomCompleter(Completer):
    def __init__(self, search_func: any):
        self.search = search_func

    def get_completions(self, document, complete_event):
        for item in self.search(document.text):
            yield Completion(
                item,
                start_position=-len(document.text_before_cursor),
            )


@dataclass
class T:

    nosay: bool = False
    lang: str = "english"
    sounds: str = "uk"
    online: bool = False
    auto: bool = True
    host = "dictionary.cambridge.org"
    platform = check_platform()

    def __post_init__(self):

        self.session = PromptSession(history=FileHistory((Path.home() / ".t_history").absolute()))
        self.main_url = f"https://{self.host}"
        self.worker = requests_html.HTMLSession()
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
        self.words_completer = WordCompleter(self.load_data())

    def load_data(self):

        if self.online:
            return []

        filename = BASE_DIR / "data" / "words_alpha.txt"
        if not filename.exists():
            print("🤔  File not found")
            sys.exit(0)
        return filename.open("r").readlines()

    def play_voice(self, url: str) -> None:
        try:
            resp = self.worker.get(url)
            assert resp.headers.get("content-type") == "audio/mpeg"
            with NamedTemporaryFile(suffix=".mp3") as file:
                file.write(resp.content)
                playsound(file.name)
        except AssertionError:
            print("🤔  Invalid audio file")
        except Exception as e:
            print(e)

    def fetch_dictionary(self):
        if not (
            word := self.session.prompt(
                "> ",
                completer=CustomCompleter(self.associate_dictionary) if self.online else self.words_completer,
                auto_suggest=AutoSuggestFromHistory(),
                enable_history_search=not self.auto,
                # complete_while_typing=False,
                style=style,
            ).strip()
        ):
            return

        resp = self.worker.get(f"{self.main_url}/search/direct/?datasetsearch={self.lang}&q={word}")
        if not (datas := Parser.dictionary(resp)):
            return
        datas["word"] = word
        self.print_words(datas)

    def associate_dictionary(self, word: str):
        resp = self.worker.get(
            f"{self.main_url}/autocomplete/amp?dataset={self.lang}&q={word}&__amp_source_origin={self.main_url}"
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
        sounds = "  ".join([f"""{y(region.upper()+'.')} {g(val['pron'])}""" for region, val in datas["sounds"].items()])

        words = f"""
{title}\t{sounds}

{m(datas['meaning'].replace(':',''))}"""

        examples = "\r\n\r\n".join(map(lambda _: c(f"🌟  {_}"), datas["examples"][:3]))
        if examples.strip():
            words += f"\r\n\r\n\r\n{examples}"

        if not self.nosay:
            self.play_voice(datas["sounds"][self.sounds]["mp3"])
        print(words)

    def start(self):
        while True:
            self.fetch_dictionary()


@click.command()
@click.option("-n", "--nosay", is_flag=True)
@click.option("--online/--offline", default=True)
@click.option("--auto/--no-auto", default=True)
@click.option(
    "-l",
    "--sounds",
    type=click.Choice(["uk", "us"], case_sensitive=False),
    default="uk",
)
def main(**kwargs):
    T(**kwargs).start()


if __name__ == "__main__":
    main()
