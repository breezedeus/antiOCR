# coding: utf-8
from typing import List, Any
import random

from pypinyin import lazy_pinyin


class AntiOcr(object):
    def __init__(self, char_reverse_ratio=0.1, char_to_pinyin_ratio=0.1):
        self.char_reverse_ratio = char_reverse_ratio
        self.char_to_pinyin_ratio = char_to_pinyin_ratio
        random.random()

    def generate(self, texts):
        if isinstance(texts, str):
            texts = self.split(texts)

        outs = self.transform(texts)
        self.render(outs)

    def split(self, texts: str) -> List[str]:
        return list(texts)

    def transform(self, texts: List[str]):
        outs = []
        for _c in texts:
            if random.random() < self.char_to_pinyin_ratio:
                _c = ''.join(lazy_pinyin(_c))
            reverse = True if random.random() < self.char_reverse_ratio else False
            outs.append((_c, reverse))
        return outs

    def render(self, outs: List[Any]):
        pass
