#!/usr/bin/env python
# -*-coding:utf-8-*-

import errno
import logging
import os.path
import subprocess
import shutil
import click
from PIL import Image

from ximage.exceptions import CommandNotFound

logger = logging.getLogger(__name__)


def mkdirs(path, mode=0o777):
    """
    Recursive directory creation function base on os.makedirs with a little error handling.
    """
    try:
        os.makedirs(path, mode=mode)
    except OSError as e:
        if e.errno != errno.EEXIST:  # File exists
            logger.error('file exists: {0}'.format(e))
            raise IOError


def convert_image(inputimg, outputformat='png', dpi=150, outputdir='',
                  outputname=''):
    """
    本函数若图片转换成功则返回目标目标在系统中的路径，否则返回None。
    文件basedir路径默认和inputimg相同，若有更进一步的需求，则考虑
    """
    pillow_support = ['png', 'jpg', 'jpeg', 'gif', 'tiff', 'bmp', 'ppm']

    inputimg = os.path.abspath(inputimg)

    imgname, imgext = os.path.splitext(os.path.basename(inputimg))
    if not os.path.exists(os.path.abspath(outputdir)):
        mkdirs(outputdir)

    # pillow
    if imgext[1:] in pillow_support and outputformat in pillow_support:
        if not outputname:
            outputname = imgname + '.' + outputformat
        outputimg = os.path.join(os.path.abspath(outputdir), outputname)

        if inputimg == outputimg:
            raise FileExistsError

        try:
            img = Image.open(inputimg)
            img.save(outputimg)
            logger.info('{0} saved.'.format(outputimg))
            return outputimg  # outputfile sometime it is useful.
        except FileNotFoundError as e:
            logger.error(
                'process image: {inputimg} raise FileNotFoundError'.format(
                    inputimg=inputimg))
        except IOError:
            logger.error('process image: {inputimg} raise IOError'.format(
                inputimg=inputimg))

    # inkscape
    elif imgext[1:] in ['svg', 'svgz'] and outputformat in ['png', 'pdf', 'ps',
                                                            'eps']:
        if not outputname:
            outputname = imgname + '.' + outputformat
        outputimg = os.path.join(os.path.abspath(outputdir), outputname)

        if inputimg == outputimg:
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
                                       '-f', inputimg, '-{0}'.format(outflag),
                                       outputimg, '-d', str(dpi)])
                return outputimg  # only retcode is zero
            else:
                raise CommandNotFound
        except CommandNotFound as e:
            logger.error('inkscape commond not found.')


    # pdftocairo
    elif imgext[1:] in ['pdf'] and outputformat in ['png', 'jpeg', 'ps', 'eps',
                                                    'svg']:
        if not outputname:
            outputname = imgname
        outputimg = os.path.join(os.path.abspath(outputdir), outputname)

        if inputimg == outputimg:
            raise FileExistsError

        try:
            if shutil.which('pdftocairo'):
                map_dict = {i: '-{}'.format(i) for i in
                            ['png', 'pdf', 'ps', 'eps', 'jpeg', 'svg']}

                outflag = map_dict[outputformat]

                if outputformat in ['png', 'jpeg']:
                    subprocess.check_call(
                        ['pdftocairo', outflag, '-singlefile', '-r', str(dpi),
                         inputimg, outputimg])
                else:
                    outputname = imgname + '.' + outputformat
                    subprocess.check_call(
                        ['pdftocairo', outflag, '-r', str(dpi), inputimg,
                         outputname])
                return outputimg  # only retcode is zero
            else:
                raise CommandNotFound
        except CommandNotFound as e:
            logger.error('pdftocairo commond not found.')


@click.command()
@click.argument('inputimgs', type=click.Path(), nargs=-1, required=True)
@click.option('--dpi', default=150, type=int, help="the output image dpi")
@click.option('--format', default="png", help="the output image format")
@click.option('--outputdir', default="", help="the image output dir")
@click.option('--outputname', default="", help="the image output name")
def main(inputimgs, dpi, format, outputdir, outputname):
    """
    support image format: \n
      - pillow : png jpg gif eps tiff bmp ppm \n
      - inkscape: svg ->pdf  png ps eps \n
      - pdftocairo: pdf ->  png jpeg ps eps svg\n
    """

    for inputimg in inputimgs:
        outputimg = convert_image(inputimg, outputformat=format, dpi=dpi,
                                  outputdir=outputdir, outputname=outputname)

        if outputimg:
            click.echo("process: {} done.".format(inputimg))
        else:
            click.echo("process: {} failed.".format(inputimg))


if __name__ == '__main__':
    main()
