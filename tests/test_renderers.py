# coding: utf-8

from antiocr.renderer import *
from antiocr.anti_ocr import AntiOcr


def test_renderer():
    renderer = Renderer()
    texts = [
        'Hello, World!你好世界123456 Hello, World!你好世界123456 ',
        'Hello, World!你好世界123456 Hello, World!你好世界123456 ',
    ]
    texts = [{'char': x} for x in '\n'.join(texts)]
    img = renderer(texts)
    img.save("output.png")


def test_anti_ocr():
    anti = AntiOcr()

    texts = [
        'Hello, World!你好世界123456 Hello, World!你好世界123456 ',
        'Hello, World!你好世界123456 Hello, World!你好世界123456 ',
    ]
    img = anti(texts, char_reverse_ratio=0.3, char_to_pinyin_ratio=0.4)
    img.save("output2.png")
