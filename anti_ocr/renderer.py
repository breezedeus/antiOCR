# coding: utf-8
from pathlib import Path
from typing import Union, Optional
import random

from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageFilter

from .consts import RESOURCE_PATH


class Renderer(object):
    def __call__(self, texts, img: Image.Image):
        # img = Image.open("data/srcimg07.jpg")  # load base image
        dctx = ImageDraw.Draw(img)  # create drawing context
        bmsz = (img.width // 16 - 10, img.height // 16 - 10)
        #
        # NOTE: ImageColor.colormap is undocumented attribute.
        colors = list(ImageColor.colormap.keys())
        for y in range(16):
            for x in range(16):
                bm = Image.new("L", bmsz)
                dctx_inner = ImageDraw.Draw(bm)
                dctx_inner.ellipse(
                    [(0, 0), bm.size],
                    fill=y * 16 + x,  # (y * 16 + x) varies in range(0, 256)
                )
                del dctx_inner

                pos = [((bmsz[0] + 10) * x + 10, (bmsz[1] + 10) * y + 10)]
                dctx.bitmap(
                    pos,
                    # pixel values of bm is used as mask to fill.
                    bm,
                    fill=colors[(y * 16 + x) % len(colors)],
                )

        # del dctx  # destroy drawing context
        # img.save("result/ImageDraw_bitmap_01.png")
        return img


def get_font_size(
    image, texts, font_fp, min_font_size, max_font_size, which_best='large'
):
    draw = ImageDraw.Draw(image)
    txt = "Hello World"
    fontsize = min_font_size  # starting font size

    # portion of image width you want text width to be
    img_fraction = 0.95

    # font = ImageFont.truetype(font_fp, fontsize)
    txtsz = draw.multiline_textsize(texts, fontsize)
    # for
    while font.getsize(txt)[0] < img_fraction * image.size[0]:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype(font_fp, fontsize)

    # optionally de-increment to be sure it is less than criteria
    fontsize -= 1
    font = ImageFont.truetype(font_fp, fontsize)

    print('final font size', fontsize)
    draw.text((10, 25), txt, font=font)  # put the text on the image
    image.save('hsvwheel_txt.png')  # save it


def rotate_char(img, _c, fnt, box, fill):
    # create image for blending
    bg_color = 'white'
    osd = Image.new("RGB", (box[2]-box[0], box[3]-box[1]), bg_color)
    draw = ImageDraw.Draw(osd)  # create drawing context
    draw.text((0, 0), _c, font=fnt, fill=fill, anchor='lt', spacing=0)  # draw text to osd
    angle = random.randint(170, 190)
    osd = osd.rotate(angle, expand=True, fillcolor=bg_color)
    del draw  # destroy drawing context

    # blend osd image
    img.paste(
        osd,
        box[:2],
        mask=Image.new("L", osd.size, 222),
    )
    return img


class Renderer2(object):
    line_break = '\n'

    def __call__(
            self,
            texts,
        min_font_size=15,
        max_font_size=60,
        font_fp='/System/Library/Fonts/PingFang.ttc',
        img: Optional[Union[Image.Image, Path, str]] = None,
    ):
        # get a font
        font_sizes = [ImageFont.truetype(font_fp, _s) for _s in range(min_font_size, max_font_size+1)]
        # fnt = None

        if img is None:
            img = Image.open(RESOURCE_PATH / 'bg2.jpeg')
        elif isinstance(img, (Path, str)):
            assert Path(img).is_file()
            img = Image.open(img)

        # 加蒙层
        # img.putalpha(Image.new("L", img.size, 52))


        # calculate text size
        draw = ImageDraw.Draw(img)  # create drawing context (of img)

        largest_box = draw.textbbox((0, 0), '藏', font_sizes[-1], anchor='lt', spacing=0)
        largest_line_height = largest_box[-1]
        # breakpoint()
        text_color = 'black'

        xy = [5, 15]
        for c_info in texts:
            start_new_line = False
            _c = c_info['char']
            if _c == self.line_break:
                start_new_line = True

            fnt = random.choice(font_sizes)

            # https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html
            spacing = random.randint(-1, 3)
            box = draw.textbbox(xy, _c, fnt, anchor='la', spacing=spacing)
            # breakpoint()

            if box[-2] > img.size[0]:
                start_new_line = True
            if start_new_line:
                xy[0] = 5
                xy[1] += largest_line_height
                box = draw.textbbox(xy, _c, fnt, anchor='la', spacing=spacing)

            if _c != self.line_break:
                if c_info['reverse']:
                    rotate_char(img, _c, fnt, box, fill=text_color)
                else:
                    draw.text(xy, _c, fill=text_color, font=fnt, anchor='la', spacing=spacing)
                xy[0] = box[-2]


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

        return img
