# coding: utf-8
from typing import List
import random
import string

from pypinyin import lazy_pinyin

from .renderer import Renderer2


class AntiOcr(object):
    def __init__(self, char_reverse_ratio=0.1, char_to_pinyin_ratio=0.1, **kwargs):
        self.char_reverse_ratio = char_reverse_ratio
        self.char_to_pinyin_ratio = char_to_pinyin_ratio
        self.renderer = Renderer2()

    def __call__(self, *args, **kwargs):
        return self.generate(*args, **kwargs)

    def generate(self, texts, bg_image=None, image_size=None, **kwargs):
        if isinstance(texts, list):
            texts = '\n'.join(texts)
        if isinstance(texts, str):
            texts = self.split(texts)

        outs = self.transform(texts)
        img = self.renderer(outs)
        return img

    def split(self, texts: str) -> List[dict]:
        ENG_LETTERS = string.digits + string.ascii_letters + string.punctuation
        outs = []
        start = 0
        _type = None
        for idx, _c in enumerate(texts):
            if _c in ENG_LETTERS and _type == 'en':
                continue
            if _type is not None:
                outs.append({'char': texts[start:idx], 'type': _type})
            start = idx
            _type = 'en' if _c in ENG_LETTERS else 'cn'

        outs.append({'char': texts[start:], 'type': _type})
        return outs

    def transform(self, texts: List[dict]):
        outs = []
        for info in texts:
            _c = info['char']
            _type = info['type']
            reverse = False
            if random.random() < self.char_to_pinyin_ratio:
                _c = ''.join(lazy_pinyin(_c))
                _type = 'pinyin'
            elif _type == 'cn':
                reverse = True if random.random() < self.char_reverse_ratio else False
            outs.append({'char': _c, 'type': _type, 'reverse': reverse})
        return outs
