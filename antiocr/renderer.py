# coding: utf-8
from pathlib import Path
from typing import Union, Optional, Dict, Any
import random

from PIL import Image, ImageDraw, ImageFont

from .consts import RESOURCE_PATH
from .utils import draw_rotated_char
from .bg_generator import BackgroundGenerator


# class Renderer0(object):
#     def __call__(self, texts, img: Image.Image):
#         # img = Image.open("data/srcimg07.jpg")  # load base image
#         dctx = ImageDraw.Draw(img)  # create drawing context
#         bmsz = (img.width // 16 - 10, img.height // 16 - 10)
#         #
#         # NOTE: ImageColor.colormap is undocumented attribute.
#         colors = list(ImageColor.colormap.keys())
#         for y in range(16):
#             for x in range(16):
#                 bm = Image.new("L", bmsz)
#                 dctx_inner = ImageDraw.Draw(bm)
#                 dctx_inner.ellipse(
#                     [(0, 0), bm.size],
#                     fill=y * 16 + x,  # (y * 16 + x) varies in range(0, 256)
#                 )
#                 del dctx_inner
#
#                 pos = [((bmsz[0] + 10) * x + 10, (bmsz[1] + 10) * y + 10)]
#                 dctx.bitmap(
#                     pos,
#                     # pixel values of bm is used as mask to fill.
#                     bm,
#                     fill=colors[(y * 16 + x) % len(colors)],
#                 )
#
#         # del dctx  # destroy drawing context
#         # img.save("result/ImageDraw_bitmap_01.png")
#         return img
#
#
# def get_font_size(
#     image, texts, font_fp, min_font_size, max_font_size, which_best='large'
# ):
#     draw = ImageDraw.Draw(image)
#     txt = "Hello World"
#     fontsize = min_font_size  # starting font size
#
#     # portion of image width you want text width to be
#     img_fraction = 0.95
#
#     # font = ImageFont.truetype(font_fp, fontsize)
#     txtsz = draw.multiline_textsize(texts, fontsize)
#     # for
#     while font.getsize(txt)[0] < img_fraction * image.size[0]:
#         # iterate until the text size is just larger than the criteria
#         fontsize += 1
#         font = ImageFont.truetype(font_fp, fontsize)
#
#     # optionally de-increment to be sure it is less than criteria
#     fontsize -= 1
#     font = ImageFont.truetype(font_fp, fontsize)
#
#     print('final font size', fontsize)
#     draw.text((10, 25), txt, font=font)  # put the text on the image
#     image.save('hsvwheel_txt.png')  # save it
#


class Renderer(object):
    line_break = '\n'

    def __init__(self):
        self.bg_generator = BackgroundGenerator()

    def __call__(
        self,
        texts,
        *,
        min_font_size=15,
        max_font_size=60,
        text_color='black',
        font_fp='/System/Library/Fonts/PingFang.ttc',
        bg_image: Optional[Union[Image.Image, Path, str]] = None,
        bg_gen_config: Optional[Dict[str, Any]] = None,
    ):
        # get a font
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
                bg_image = Image.open(RESOURCE_PATH / 'bg.jpeg')
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
                if c_info['reverse']:
                    draw_rotated_char(bg_image, _c, fnt, box, fill=text_color)
                else:
                    draw.text(
                        xy, _c, fill=text_color, font=fnt, anchor='la', spacing=spacing
                    )
                xy[0] = box[-2]

        height = min(xy[1] + largest_line_height * 1.5, bg_image.size[1])
        bg_image = bg_image.crop((0, 0, min(bg_image.size[0], max_width + 5), height))

        # txtsz = draw.multiline_textsize(texts, fnt)
        # # breakpoint()
        # # del dctx
        #
        # # create image for blending
        # osd = Image.new("RGB", (txtsz[0] + 10, txtsz[1] + 10), 245)
        # draw = ImageDraw.Draw(osd)  # create drawing context
        # draw.multiline_text((5, 5), texts, font=fnt, fill="red")  # draw text to osd
        # del draw  # destroy drawing context
        #
        # # blend osd image
        # img.paste(
        #     osd,
        #     box=(20, 420, osd.size[0] + 20, osd.size[1] + 420),
        #     mask=Image.new("L", osd.size, 192),
        # )

        # # draw text to mask
        # mask = Image.new("L", (txtsz[0], txtsz[1]), 12)
        # dctx = ImageDraw.Draw(mask)  # create drawing context (of mask)
        # dctx.multiline_text((0, 0), texts, font=fnt, fill=255)  # full opacity
        #
        # del dctx  # destroy drawing context
        #
        # # add some effect
        # for i in range(10):
        #     mask = mask.filter(ImageFilter.BLUR)
        #
        # # putmask to base image
        # img.putalpha(mask.resize(img.size))

        return bg_image