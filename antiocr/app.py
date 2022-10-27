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

from PIL import Image
import streamlit as st

from cnocr import CnOcr
from cnocr.utils import set_logger

from antiocr.anti_ocr import AntiOcr

logger = set_logger()
st.set_page_config(layout="wide")

FONT_FP = '/System/Library/Fonts/PingFang.ttc'


@st.cache(allow_output_mutation=True)
def get_ocr_model():
    return CnOcr()


def main():
    st.sidebar.header('输出设置')
    char_reverse_ratio = st.sidebar.slider(
        '文字倒转概率', min_value=0.0, max_value=1.0, value=0.3
    )
    char_to_pinyin_ratio = st.sidebar.slider(
        '文字转拼音概率', min_value=0.0, max_value=1.0, value=0.3
    )
    cols = st.sidebar.columns(2)
    min_font_size = int(cols[0].number_input('最小文字大小', 2, 80, value=15))
    max_font_size = int(
        cols[1].number_input('最大文字大小', min_font_size + 1, 120, value=max(60, min_font_size+1))
    )
    text_color = st.sidebar.color_picker('文字颜色')

    st.markdown('# 让文字自由传播：[antiOCR](https://github.com/breezedeus/antiOCR)')
    st.markdown(
        '**antiOCR** 对指定的文字（来自输入或者图片）进行处理，输出图片，此图片无法通过OCR技术识别出有意义的文字。'
    )
    st.markdown(
        '> 欢迎加入 [交流群](https://cnocr.readthedocs.io/zh/latest/contact/) ；'
        '作者：[breezedeus](https://github.com/breezedeus) 。'
    )
    st.markdown('')
    st.subheader('选择待转换文字图片，或者直接输入待转换文字')
    default_texts = '不过中国的有一些士大夫，总爱无中生有，移花接木的造出故事来，他们不但歌颂升平，还粉饰黑暗。关于铁氏二女的撒谎，尚其小焉者耳，大至胡元杀掠，满清焚屠之际，也还会有人单单捧出什么烈女绝命，难妇题壁的诗词来，这个艳传，那个步韵，比对于华屋丘墟，生民涂炭之惨的大事情还起劲。 ——鲁迅'
    content_file = st.file_uploader('待转换文字图片', type=["png", "jpg", "jpeg", "webp"])
    ocr = get_ocr_model()
    anti = AntiOcr()
    texts = None
    if content_file is not None:
        try:
            img = Image.open(content_file).convert('RGB')
            ocr_out = ocr.ocr(img)
            texts = '\n'.join([out['text'] for out in ocr_out])
        except Exception as e:
            st.error(e)

    texts = st.text_area('待转换文字图片', value=texts or default_texts, height=120)

    if st.button("生成图片"):
        if texts:
            out_img = anti(
                texts,
                char_reverse_ratio=char_reverse_ratio,
                char_to_pinyin_ratio=char_to_pinyin_ratio,
                text_color=text_color,
                min_font_size=min_font_size,
                max_font_size=max_font_size,
            )
            st.subheader('输出图片')
            st.image(out_img)
            st.markdown('**对输出图片进行OCR，结果如下（如果依旧出现敏感词，尝试重新生成图片）：**')
            ocr_out = ocr.ocr(out_img)
            new_texts = [out['text'] for out in ocr_out]
            st.text('\n'.join(new_texts))


if __name__ == '__main__':
    main()
