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
import os.path
from pathlib import Path
from typing import Union, Optional, Dict, Any
import random

from PIL import Image, ImageDraw, ImageFont

from .consts import BG_IMAGE_FP
from .utils import draw_rotated_char
from .bg_generator import BackgroundGenerator


class Renderer(object):
    line_break = '\n'

    def __init__(self):
        self.bg_generator = BackgroundGenerator()

    def __call__(
        self,
        texts,
        *,
        font_fp,
        min_font_size=15,
        max_font_size=60,
        text_color='black',
        bg_image: Optional[Union[Image.Image, Path, str]] = None,
        bg_gen_config: Optional[Dict[str, Any]] = None,
    ):
        # get a font
        assert os.path.isfile(font_fp)
        font_sizes = [
            ImageFont.truetype(font_fp, _s)
            for _s in range(min_font_size, max_font_size + 1)
        ]
        # fnt = None

        if bg_image is None:
            default_bg_gen_config = dict(
                image_size=(800, 700),
                min_font_size=int(min_font_size * 0.5),
                max_font_size=int(max_font_size * 0.8),
                text_density=1,
                text_color=text_color,
                font_fps=[font_fp],
            )
            bg_gen_config = bg_gen_config or dict()
            default_bg_gen_config.update(bg_gen_config)
            try:
                bg_image = self.bg_generator(**default_bg_gen_config)
            except:
                bg_image = Image.open(BG_IMAGE_FP)
        elif isinstance(bg_image, (Path, str)):
            assert Path(bg_image).is_file()
            bg_image = Image.open(bg_image)

        # 加蒙层
        # img.putalpha(Image.new("L", img.size, 52))
        img_ori = bg_image.copy()

        # calculate text size
        draw = ImageDraw.Draw(bg_image)  # create drawing context (of img)

        largest_box = draw.textbbox((0, 0), '中', font_sizes[-1], anchor='lt', spacing=0)
        largest_line_height = largest_box[-1]

        xy = [5, 15]
        max_width = 5
        for c_info in texts:
            start_new_line = False
            _c = c_info['char']
            if _c == self.line_break:
                start_new_line = True

            fnt = random.choice(font_sizes)

            # https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html
            spacing = random.randint(-1, 3)
            box = draw.textbbox(xy, _c, fnt, anchor='la', spacing=spacing)
            max_width = max(max_width, box[-2])

            if box[-2] > bg_image.size[0]:
                start_new_line = True
            if start_new_line:
                xy[0] = 5
                xy[1] += largest_line_height
                box = draw.textbbox(xy, _c, fnt, anchor='la', spacing=spacing)

            if box[-1] >= bg_image.size[1]:
                # 竖向扩展图片
                new_img = Image.new(
                    'RGB',
                    (img_ori.size[0], bg_image.size[1] + img_ori.size[1]),
                    (255, 255, 255),
                )
                new_img.paste(bg_image, (0, 0))
                new_img.paste(img_ori, (0, bg_image.size[1]))
                bg_image = new_img
                draw = ImageDraw.Draw(bg_image)

            if _c != self.line_break:
                if c_info.get('reverse', False):
                    draw_rotated_char(bg_image, _c, fnt, box, fill=text_color)
                else:
                    draw.text(
                        xy, _c, fill=text_color, font=fnt, anchor='la', spacing=spacing
                    )
                xy[0] = box[-2]

        height = min(xy[1] + largest_line_height * 1.5, bg_image.size[1])
        bg_image = bg_image.crop((0, 0, min(bg_image.size[0], max_width + 5), height))

        return bg_image
