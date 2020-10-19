import sys

import requests_html
from requests.sessions import session

from t.log import error


def check_platform() -> dict:
    return {
        "darwin": {"audio": "afplay {}"},
        "linux": {"audio": ""},
        "win32": {"audio": ""},
    }[sys.platform]


def check_langs() -> list:
    session, langs = requests_html.HTMLSession(), {"english"}
    try:
        langs = langs.union(
            set(
                session.get("https://dictionary.cambridge.org/").html.xpath(
                    "//a[@data-dictcode]/@data-dictcode"
                )
            )
        )
    except Exception as e:
        error(e)
    return session, tuple(sorted(langs))
