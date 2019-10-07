#!/usr/bin/env python
# -*-coding:utf-8-*-


from ximage.convert_image import convert_image

outimg = convert_image('中文.pdf', pdftocairo_fix_encoding='gb18030', overwrite=False)

print(outimg)
