from dataclasses import dataclass
from urllib.parse import urljoin


class Parser:
    @staticmethod
    def dictionary(resp) -> dict:
        if not (targets := resp.html.xpath('//div[@class="pr dictionary"][1]//div[@class="pr entry-body__el"][1]')):
            return {}

        target = targets[0]
        sounds = {
            _.xpath('//span[contains(@class,"region")]/text()')[0]: {
                "mp3": urljoin(resp.url, audios[0])
                if (audios := _.xpath('//source[@type="audio/mpeg"]/@src'))
                else None,
                "pron": prons[0] if (prons := _.xpath('//span[contains(@class,"ipa")]/text()')) else None,
            }
            for _ in target.xpath('//span[contains(@class,"dpron-i")]')
        }

        meaning = target.xpath('//div[contains(@class,"ddef_d")]')[0].text
        examples = [
            item.text for item in target.xpath('//div[@class="def-body ddef_b"]//div[contains(@class,"dexamp")]')
        ]
        # breakpoint()
        return {"sounds": sounds, "meaning": meaning, "examples": examples}

    @staticmethod
    def associate(resp) -> list:
        return [_["word"] for _ in resp.json()]
