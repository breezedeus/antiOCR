# coding: utf-8
from pathlib import Path
from typing import List, Union, Tuple, Optional
import random
import string

from PIL import Image
from pypinyin import lazy_pinyin

from .renderer import Renderer

ENG_LETTERS = string.digits + string.ascii_letters + string.punctuation


class AntiOcr(object):
    def __init__(self, **kwargs):
        self.renderer = Renderer()

    def __call__(
        self,
        texts: Union[str, List[str]],
        *,
        char_to_pinyin_ratio: float = 0.1,
        char_reverse_ratio: float = 0.1,
        min_font_size: int = 15,
        max_font_size: int = 60,
        text_color: Union[str, int, Tuple[int, int, int]] = 'black',
        bg_image: Optional[Union[str, Path, Image.Image]] = None,
        font_fp: Union[str, Path] = '/System/Library/Fonts/PingFang.ttc',
        **kwargs
    ):
        """

        Args:
            texts (Union[str, List[str]]): 待转换文字文字
            char_to_pinyin_ratio (float): 中文字符转换成拼音的比例；默认值为 `0.1`
            char_reverse_ratio (float): 中文字符倒转的比例（拼音、英文和数字不做倒转）；默认值为 `0.1`
            min_font_size (int): 转换后的文字字体最小值；默认值为 `15`
            max_font_size (int): 转换后的文字字体最大值；默认值为 `60`
            text_color (Union[str, int, Tuple[int, int, int]]): 转换后的文字颜色；默认值为 `black`
            bg_image (Optional[Union[str, Path, Image.Image]]): 背景图片；默认值为 `None`，表示使用默认背景图片
            font_fp (Union[str, Path]): 字体文件所在路径；默认值为 `/System/Library/Fonts/PingFang.ttc` (MAC)
            **kwargs ():

        Returns:

        """
        if isinstance(texts, list):
            texts = '\n'.join(texts)
        if isinstance(texts, str):
            texts = self.split(texts)

        outs = self.transform(texts, char_to_pinyin_ratio, char_reverse_ratio)
        img = self.renderer(
            outs,
            min_font_size=min_font_size,
            max_font_size=max_font_size,
            text_color=text_color,
            font_fp=font_fp,
            bg_image=bg_image,
        )
        return img

    @classmethod
    def split(cls, texts: str) -> List[dict]:
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

    @classmethod
    def transform(cls, texts: List[dict], char_to_pinyin_ratio, char_reverse_ratio):
        outs = []
        for info in texts:
            _c = info['char']
            _type = info['type']
            reverse = False
            if random.random() < char_to_pinyin_ratio:
                _c = ''.join(lazy_pinyin(_c))
                _type = 'pinyin'
            elif _type == 'cn':
                reverse = True if random.random() < char_reverse_ratio else False
            outs.append({'char': _c, 'type': _type, 'reverse': reverse})
        return outs
