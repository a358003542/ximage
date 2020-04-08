#!/usr/bin/env python
# -*-coding:utf-8-*-


from ximage.convert_image import convert_image

outimg = convert_image('other_folder/中文2.pdf', outputdir='other_folder',pdftocairo_fix_encoding='gb18030', overwrite=False)

print(outimg)

outimg = convert_image('other_folder/中文3.pdf', outputdir='other_folder',pdftocairo_fix_encoding='gb18030', overwrite=False)

print(outimg)

outimg = convert_image('other_folder/other_folder2/中文4.pdf', outputdir='other_folder/other_folder2',pdftocairo_fix_encoding='gb18030', overwrite=False)

print(outimg)

outimg = convert_image('other_folder/other_folder2/中文5.pdf', outputdir='other_folder/other_folder2',pdftocairo_fix_encoding='gb18030', overwrite=False)

print(outimg)