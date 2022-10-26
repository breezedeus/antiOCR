# coding: utf-8

from anti_ocr.renderer import *
from anti_ocr.anti_ocr import AntiOcr


def test_renderer2():
    renderer = Renderer2()
    texts = [
        'Hello, World!你好世界123456 Hello, World!你好世界123456 ',
        'Hello, World!你好世界123456 Hello, World!你好世界123456 ',
    ]
    texts = [{'char': x} for x in '\n'.join(texts)]
    img = renderer(texts)
    img.save("output.png")


def test_anti_ocr():
    anti = AntiOcr(char_reverse_ratio=0.3, char_to_pinyin_ratio=0.4)

    texts = [
        'Hello, World!你好世界123456 Hello, World!你好世界123456 ',
        'Hello, World!你好世界123456 Hello, World!你好世界123456 ',
    ]
    img = anti(texts)
    img.save("output2.png")
