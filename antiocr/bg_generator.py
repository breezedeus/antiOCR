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

import os
from pathlib import Path
from typing import Union, Optional, List
import random
import string

from PIL import Image, ImageDraw, ImageFont, ImageFilter

from .utils import draw_rotated_char

ENG_LETTERS = string.digits + string.ascii_letters + string.punctuation


class BackgroundGenerator(object):
    def __call__(
        self,
        image_size=(512, 512),
        *,
        font_fps: List[Union[str, Path]],
        image_color=(255, 255, 255),
        min_font_size=15,
        max_font_size=60,
        text_density=1,
        text_color=(64, 64, 64),
        bg_image: Optional[Union[Image.Image, Path, str]] = None,
        filter_fn=ImageFilter.MaxFilter(3),
        **kwargs,
    ):
        if bg_image is None:
            bg_image = Image.new('RGB', image_size, image_color)
        draw = ImageDraw.Draw(bg_image)

        image_size = bg_image.size

        num_letters = int(0.008 * text_density * image_size[0] * image_size[1])
        for idx in range(num_letters):
            _c = random.choice(ENG_LETTERS)
            fnt_size = random.randint(min_font_size, max_font_size)
            fnt_fp = random.choice(font_fps)
            assert os.path.isfile(fnt_fp)
            fnt = ImageFont.truetype(fnt_fp, fnt_size)
            xy = (random.randint(0, image_size[0]), random.randint(0, image_size[1]))
            box = draw.textbbox(xy, _c, fnt, anchor='la', spacing=0)
            draw_rotated_char(
                bg_image,
                _c,
                fnt,
                box,
                fill=text_color,
                stroke_width=1,
                angle_range=(0, 360),
            )

        if filter_fn is not None:
            bg_image = bg_image.filter(filter_fn)
        return bg_image
