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

from antiocr.bg_generator import BackgroundGenerator


def test_anti_ocr():
    generator = BackgroundGenerator()

    img = generator(
        image_size=(1280, 768),
        font_fps=['/System/Library/Fonts/PingFang.ttc'],
        min_font_size=15,
        max_font_size=30,
        text_density=1,
        text_color=(0, 0, 0),
    )
    img.save("bg.png")
