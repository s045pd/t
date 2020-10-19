from dataclasses import dataclass
from urllib.parse import urljoin


class Parser:
    @staticmethod
    def dictionary(resp):
        target = resp.html.xpath(
            '//div[@class="pr dictionary"][1]//div[@class="pr entry-body__el"][1]'
        )[0]
        sounds = {
            _.xpath('//span[contains(@class,"region")]/text()')[0]: {
                "mp3": urljoin(
                    resp.url, _.xpath('//source[@type="audio/mpeg"]/@src')[0]
                ),
                "pron": f"""/{_.xpath('//span[contains(@class,"ipa")]/text()')[0] }/""",
            }
            for _ in target.xpath('//span[contains(@class,"dpron-i")]')
        }

        meaning = target.xpath('//div[contains(@class,"ddef_d")]')[0].text
        examples = [
            item.text
            for item in target.xpath(
                '//div[@class="def-body ddef_b"]//div[contains(@class,"dexamp")]'
            )
        ]
        return {"sounds": sounds, "meaning": meaning, "examples": examples}

    @staticmethod
    def associate(resp):
        return [_["word"] for _ in resp.json()]
