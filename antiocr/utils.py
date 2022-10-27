# coding: utf-8
import random

from PIL import Image, ImageDraw


def draw_rotated_char(img, _c, fnt, box, fill, stroke_width=0, angle_range=(170, 190)):
    # create image for blending
    bg_color = 'white'
    osd = Image.new("RGB", (box[2] - box[0], box[3] - box[1]), bg_color)
    draw = ImageDraw.Draw(osd)  # create drawing context
    draw.text(
        (0, 0), _c, font=fnt, fill=fill, anchor='lt', spacing=0, stroke_width=stroke_width
    )  # draw text to osd
    angle = random.randint(angle_range[0], angle_range[1])
    osd = osd.rotate(angle, expand=True, fillcolor=bg_color)
    del draw  # destroy drawing context

    # blend osd image
    img.paste(
        osd, box[:2], mask=Image.new("L", osd.size, 254),
    )
    return img
