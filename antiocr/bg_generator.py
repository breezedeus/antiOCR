# coding: utf-8
from pathlib import Path
from typing import Union, Optional
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
        image_color=(255, 255, 255),
        min_font_size=15,
        max_font_size=60,
        text_density=1,
        text_color=(64, 64, 64),
        font_fps=['/System/Library/Fonts/PingFang.ttc'],
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
