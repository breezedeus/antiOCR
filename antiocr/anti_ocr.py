# coding: utf-8
# Copyright (C) 2022, [Breezedeus](https://github.com/breezedeus).
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

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
        font_fp: Union[str, Path],
        char_to_pinyin_ratio: float = 0.1,
        char_reverse_ratio: float = 0.1,
        min_font_size: int = 15,
        max_font_size: int = 60,
        text_color: Union[str, int, Tuple[int, int, int]] = 'black',
        bg_image: Optional[Union[str, Path, Image.Image]] = None,
        **kwargs
    ) -> Image.Image:
        """

        Args:
            texts (Union[str, List[str]]): 待转换文字文字
            font_fp (Union[str, Path]): 字体文件所在路径；比如Mac下可以是 `/System/Library/Fonts/PingFang.ttc`
            char_to_pinyin_ratio (float): 中文字符转换成拼音的比例；默认值为 `0.1`
            char_reverse_ratio (float): 中文字符倒转的比例（拼音、英文和数字不做倒转）；默认值为 `0.1`
            min_font_size (int): 转换后的文字字体最小值；默认值为 `15`
            max_font_size (int): 转换后的文字字体最大值；默认值为 `60`
            text_color (Union[str, int, Tuple[int, int, int]]): 转换后的文字颜色；默认值为 `black`
            bg_image (Optional[Union[str, Path, Image.Image]]): 背景图片；默认值为 `None`，表示使用默认背景图片
            **kwargs (): 可包括以下 key，
              * `bg_gen_config`: dict, 传给 `BackgroundGenerator` 的调用参数

        Returns: Image.Image, 生成的图片

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
            bg_gen_config=kwargs.get('bg_gen_config', dict()),
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
