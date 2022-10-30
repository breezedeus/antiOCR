# antiOCR

**Anti OCR, Free Texts.**

拒绝图片文字被OCR，让文字自由传播！  **antiOCR** 把指定文本转换成机器无法识别但人可读的文字图片。



欢迎扫码加小助手为好友，备注 `anti`，小助手会定期统一邀请大家入群：

<div align="center">
  <img src="./docs/figs/wx-qr-code.JPG" alt="微信群二维码" width="300px"/>
</div>


作者也维护 **知识星球** [**P2T/CnOCR/CnSTD私享群**](https://t.zsxq.com/FEYZRJQ) ，这里面的提问会较快得到作者的回复，欢迎加入。**知识星球私享群**也会陆续发布一些P2T/CnOCR/CnSTD相关的私有资料，包括[**更详细的训练教程**](https://articles.zsxq.com/id_u6b4u0wrf46e.html)，**未公开的模型**，**不同应用场景的调用代码**，使用过程中遇到的难题解答等。本群也会发布OCR/STD相关的最新研究资料。



## 使用说明


调用很简单，以下是示例：

```python
from antiocr import AntiOcr

texts = '拒绝图片文字被OCR，让文字自由传播！  antiOCR 把指定文本转换成机器无法识别但人可读的文字图片。'
anti = AntiOcr()

# 生成文字图片
img = anti(
    texts,
    font_fp='/System/Library/Fonts/PingFang.ttc',  # 使用的字体文件
)
img.save("output.png")

```



## 安装

嗯，顺利的话一行命令即可。

```bash
pip install antiocr
```

安装速度慢的话，可以指定国内的安装源，如使用豆瓣源：

```bash
pip install antiocr -i https://pypi.doubanio.com/simple
```



## 给作者来杯咖啡

开源不易，如果此项目对您有帮助，可以考虑 [给作者加点油🥤，鼓鼓气💪🏻](https://cnocr.readthedocs.io/zh/latest/buymeacoffee/) 。

---

官方代码库：[https://github.com/breezedeus/antiocr](https://github.com/breezedeus/antiocr)。
