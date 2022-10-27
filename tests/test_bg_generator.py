# coding: utf-8

from antiocr.bg_generator import BackgroundGenerator


def test_anti_ocr():
    generator = BackgroundGenerator()

    img = generator(
        image_size=(1280, 768),
        min_font_size=15,
        max_font_size=30,
        text_density=1,
        text_color=(0, 0, 0),
    )
    img.save("bg.png")
