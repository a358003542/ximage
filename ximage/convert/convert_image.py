#!/usr/bin/env python
# -*-coding:utf-8-*-


import logging
import os.path
import subprocess
import shutil
import click
from PIL import Image

from ximage.exceptions import CommandNotFound

logger = logging.getLogger(__name__)




def convert_image(inputimg, outputformat='png', dpi=150):
    """
    本函数若图片转换成功则返回目标目标在系统中的路径，否则返回None。
    文件basedir路径默认和inputimg相同，若有更进一步的需求，则考虑
    """

    pillow_support = ['png', 'jpg', 'jpeg','gif', 'eps', 'tiff', 'bmp', 'ppm']

    inputname, inputext = os.path.splitext(inputimg)

    # pillow
    if inputext[1:] in pillow_support and outputformat in pillow_support:
        outputfile = inputname + '.' + outputformat

        if inputimg == outputfile:
            raise FileExistsError

        try:
            Image.open(inputimg).save(outputfile)
            return outputfile # outputfile sometime it is useful.
        except IOError:
            logger.error('process image: {inputimg} raise IOError'.format(inputimg=inputimg))
            return None

    # inkscape
    elif inputext[1:] in ['svg', 'svgz'] and outputformat in ['png', 'pdf', 'ps', 'eps']:
        outputfile = inputname + '.' + outputformat

        if inputimg == outputfile:
            raise FileExistsError

        if outputformat == 'png':
            outflag = 'e'
        elif outputformat == 'pdf':
            outflag = 'A'
        elif outputformat == 'ps':
            outflag = 'P'
        elif outputformat == 'eps':
            outflag = 'E'

        try:
            if shutil.which('inkscape'):
                subprocess.check_call(['inkscape', '-zC',
                             '-f', inputimg, '-{0}'.format(outflag), outputfile, '-d', str(dpi)])
                return outputfile # only retcode is zero
            else:
                raise CommandNotFound
        except Exception as e:
            logger.error(e)
            return None

    # pdftoppm
    elif inputext[1:] in ['pdf'] and outputformat in ['png']:
        outputfile = inputname + '.' + outputformat

        if inputimg == outputfile:
            raise FileExistsError

        try:
            if shutil.which('pdftoppm'):
                subprocess.check_call(['pdftoppm', '-png', '-singlefile', '-r', str(dpi), inputimg, inputname])
                return outputfile # only retcode is zero
            else:
                raise CommandNotFound
        except Exception as e:
            logger.error(e)
            return None

    # pdf2svg
    elif inputext[1:] in ['pdf'] and outputformat in ['svg']:
        outputfile = inputname + '.' + outputformat

        if inputimg == outputfile:
            raise FileExistsError

        try:
            if shutil.which('pdf2svg'):
                subprocess.check_call(['pdf2svg', inputimg, outputfile])
                return outputfile  # only retcode is zero
            else:
                raise CommandNotFound
        except Exception as e:
            logger.error(e)
            return None
    else:
        raise NotImplementedError


@click.command()
@click.argument('inputimgs', type=click.Path(), nargs=-1, required=True)
@click.option('--dpi', default=150, type=int, help="the output image dpi")
@click.option('--format', default="png", help="the output image format")
def main(inputimgs, dpi, format):
    """
    support image format: \n
      - pillow : png jpg gif eps tiff bmp ppm \n
      - inkscape: svg ->pdf  png ps eps \n
      - pdftoppm: pdf ->  png \n
      - pdf2svg: pdf ->  svg
    """

    for inputimg in inputimgs:
        outputimg = convert_image(inputimg, outputformat=format, dpi=dpi)

        if outputimg:
            click.echo("process: {} done.".format(inputimg))
        else:
            click.echo("process: {} failed.".format(inputimg))



if __name__ == '__main__':
    main()
