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
    texts = """
    栗战书在向胡锦涛解释的时候，王沪宁也在帮腔，向胡锦涛摆手做出“不要”的手势，所以他和栗战书一样知道是怎么回事，就是我说的，此前已经发生冲突了。另外，五毛水军现在又发明了一个说法，说是胡锦涛违反了会议规定，表决前不能打开看。至于习近平、汪洋前面的文件都是公开放着的，五毛们就装看不到了
    """
    img = anti(texts)
    img.save("output2.png")
