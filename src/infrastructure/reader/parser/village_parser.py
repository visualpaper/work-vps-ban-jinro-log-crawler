from typing import Optional

from bs4 import BeautifulSoup

from src.domain.shared.village import Village


class VillageParser:
    def parse(self, content: bytes) -> Optional[Village]:
        soup = BeautifulSoup(
            content,
            'html.parser',
            from_encoding='utf-8',
            exclude_encodings=[],
        )
        # もし、original が想定 encoding と異なる場合(今回は utf-8) に、
        # exclude_encodings に以下を設定することで解決できるケースがある。
        # ※ 指定しなければ response ヘッダの encoding が利用され、うまくパースできないことがあり、
        #    その解決策としてこのような方法をとっている。
        # print(soup.original_encoding)
        #
        # そのまま html 出力したい場合は以下で可能
        #print(str(soup))
        return None
