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

import os

from PIL import Image, ImageFilter
import streamlit as st

from cnocr import CnOcr

from antiocr import AntiOcr, BG_IMAGE_FP, FONT_NAMES, set_logger, download_font

logger = set_logger()
st.set_page_config(layout="wide")
FONT_LOCAL_DIR = 'fonts'


@st.cache(allow_output_mutation=True)
def get_ocr_model():
    return CnOcr()


def download_image_button(img):
    from io import BytesIO

    buf = BytesIO()
    img.save(buf, format="JPEG")
    byte_im = buf.getvalue()
    st.download_button(
        label="下载图片", data=byte_im, file_name="antiOCR.jpeg", mime="image/jpeg",
    )


def main():
    st.sidebar.header('输出设置')

    with st.spinner('Downloading fonts ...'):
        for fnt_fp in FONT_NAMES:
            download_font(os.path.join(FONT_LOCAL_DIR, fnt_fp))

    font_fn = st.sidebar.selectbox('选择字体', FONT_NAMES, index=0)
    font_fp = os.path.join(FONT_LOCAL_DIR, font_fn)
    char_reverse_ratio = st.sidebar.slider(
        '文字倒转概率', min_value=0.0, max_value=1.0, value=0.1
    )
    char_to_pinyin_ratio = st.sidebar.slider(
        '文字转拼音概率', min_value=0.0, max_value=1.0, value=0.1
    )
    cols = st.sidebar.columns(2)
    min_font_size = int(cols[0].number_input('最小文字大小', 2, 80, value=15))
    max_font_size = int(
        cols[1].number_input(
            '最大文字大小', min_font_size + 1, 120, value=max(40, min_font_size + 1)
        )
    )
    text_color = st.sidebar.color_picker('文字颜色', value='#5087DC')

    st.sidebar.markdown('----')
    use_random_bg = st.sidebar.checkbox('随机生成背景图片')
    if use_random_bg:
        bg_text_density = st.sidebar.slider(
            '背景图片文字密度', min_value=0.0, max_value=3.0, value=1.0
        )
        cols = st.sidebar.columns(2)
        bg_min_size = int(
            cols[0].number_input('背景图片最小文字', 2, 80, key='bg_min', value=15)
        )
        bg_max_size = int(
            cols[1].number_input(
                '背景图片最大文字',
                bg_min_size + 1,
                120,
                key='bg_max',
                value=max(70, bg_min_size + 1),
            )
        )
        bg_text_color = st.sidebar.color_picker('背景图片文字颜色', value='#07BCE0')
        bg_gen_config = dict(
            text_density=bg_text_density,
            text_color=bg_text_color,
            min_font_size=bg_min_size,
            max_font_size=bg_max_size,
        )
        bg_image = None
    else:
        bg_gen_config = None
        bg_image = Image.open(BG_IMAGE_FP)
        bg_image = bg_image.filter(ImageFilter.MaxFilter(3))

    title = '让文字自由传播：<a href="https://github.com/breezedeus/antiOCR">antiOCR</a>'
    st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
    subtitle = (
        '作者：<a href="https://github.com/breezedeus">breezedeus</a>； '
        '欢迎加入 <a href="https://cnocr.readthedocs.io/zh/latest/contact/">交流群</a>'
    )
    st.markdown(
        f"<div style='text-align: center;'>{subtitle}</div>", unsafe_allow_html=True
    )
    st.markdown('')
    st.markdown('')
    desc = '<strong>antiOCR</strong> 对指定的文字（来自输入或者图片）进行处理，输出图片，此图片无法通过OCR技术识别出有意义的文字。'
    st.markdown(f"<div style='text-align: left;'>{desc}</div>", unsafe_allow_html=True)
    st.markdown('')
    st.subheader('选择待转换文字图片，或者直接输入待转换文字')
    default_texts = '真的猛士，敢于直面惨淡的人生，敢于正视淋漓的鲜血。这是怎样的哀痛者和幸福者？然而造化又常常为庸人设计，以时间的流逝，来洗涤旧迹，仅是留下淡红的血色和微漠的悲哀。在这淡红的血色和微漠的悲哀中，又给人暂得偷生，维持着这似人非人的世界。 ——鲁迅'
    content_file = st.file_uploader('输入待转换的文字图片：', type=["png", "jpg", "jpeg", "webp"])
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

    texts = st.text_area('或者，直接输入待转换的文字：', value=texts or default_texts, height=120)

    if st.button("生成图片"):
        if texts:
            with st.spinner('图片生成中…'):
                out_img = anti(
                    texts,
                    char_reverse_ratio=char_reverse_ratio,
                    char_to_pinyin_ratio=char_to_pinyin_ratio,
                    text_color=text_color,
                    min_font_size=min_font_size,
                    max_font_size=max_font_size,
                    bg_image=bg_image,
                    bg_gen_config=bg_gen_config,
                    font_fp=font_fp,
                )
            st.subheader('输出图片')
            st.image(out_img)
            download_image_button(out_img)

            st.markdown('**对输出图片进行OCR，结果如下（如果依旧出现敏感词，尝试重新生成图片）：**')
            ocr_out = ocr.ocr(out_img)
            new_texts = [out['text'] for out in ocr_out]
            st.text('\n'.join(new_texts))


if __name__ == '__main__':
    main()
