from typing import Optional

from bs4 import BeautifulSoup

from src.domain.shared.village import Village


class VillageParser:
    def parse(self, content: bytes) -> Optional[Village]:
        soup = BeautifulSoup(
            content,
            'html.parser',
            from_encoding='euc-jp',
            exclude_encodings=[
                "iso8859_16",
                "iso-8859-5",
                "mac_latin2",
                "windows-1252",
                "iso8859_13",
                "windows-1250",
                "mac_iceland",
                "euc_jis_2004",
                "mac_roman",
                "iso8859_4",
                "gb18030",
                "ptcp154",
                "maccyrillic",
                "mac_greek",
            ],
        )
        print(soup.original_encoding)
        return None
