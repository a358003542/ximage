#!/usr/bin/env python
# -*-coding:utf-8-*-

import sys
import errno
import logging
import os.path
import subprocess
import shutil
import click
from PIL import Image
import random
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


def convert_encoding(origin_s, origin_encoding, to_encoding,
                     errors='ignore'):
    b = origin_s.encode(origin_encoding, errors=errors)
    s = b.decode(to_encoding, errors)
    return s


def detect_output_file_exist(basedir, imgname, outputformat, overwrite):
    filename = '{}.{}'.format(imgname, outputformat)
    filename = os.path.join(basedir, filename)

    if os.path.exists(filename) and not overwrite:
        click.echo('output image file exists. i will give it up.')
        return None
    return filename


def convert_image(inputimg, outputformat='png', dpi=150, outputdir='',
                  outputname='', pdftocairo_fix_encoding='',
                  overwrite=True):
    """
    本函数若图片转换成功则返回目标目标在系统中的路径，否则返回None。
    文件basedir路径默认和inputimg相同，若有更进一步的需求，则考虑
    """
    pillow_support = ['png', 'jpg', 'jpeg', 'gif', 'tiff', 'bmp', 'ppm']

    inputimg = os.path.abspath(inputimg)

    basedir = os.path.abspath(outputdir)
    if not os.path.exists(basedir):
        mkdirs(basedir)

    imgname, imgext = os.path.splitext(os.path.basename(inputimg))

    if not outputname:
        outputname = imgname + '.{}'.format(outputformat)
        output_imgname = imgname
    else:
        output_imgname, ext = os.path.splitext(outputname)
        if not ext:
            outputname = output_imgname + '.{}'.format(outputformat)
        elif ext != outputformat:
            raise Exception(
                'outputname ext is not the same as the outputformat')

    # pillow
    if imgext[1:] in pillow_support and outputformat in pillow_support:
        outputimg = detect_output_file_exist(basedir, output_imgname,
                                             outputformat,
                                             overwrite)
        if not outputimg:
            return None

        if inputimg == outputimg:
            raise FileExistsError

        try:
            img = Image.open(inputimg)
            img.save(outputimg)
            click.echo('{0} saved.'.format(outputimg))
            return outputimg  # outputfile sometime it is useful.
        except FileNotFoundError as e:
            click.echo(
                'process image: {inputimg} raise FileNotFoundError'.format(
                    inputimg=inputimg), err=True)
        except IOError:
            click.echo('process image: {inputimg} raise IOError'.format(
                inputimg=inputimg), err=True)

    # inkscape
    elif imgext[1:] in ['svg', 'svgz'] and outputformat in ['png', 'pdf', 'ps',
                                                            'eps']:
        outputimg = detect_output_file_exist(basedir, output_imgname,
                                             outputformat,
                                             overwrite)
        if not outputimg:
            return None

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
            click.echo('inkscape commond not found.', err=True)


    # pdftocairo
    elif imgext[1:] in ['pdf'] and outputformat in ['png', 'jpeg', 'ps', 'eps',
                                                    'svg']:
        outputimg = detect_output_file_exist(basedir, output_imgname,
                                             outputformat,
                                             overwrite)
        if not outputimg:
            return None

        currdir = os.curdir
        if outputdir:
            os.chdir(outputdir)

        try:
            if shutil.which('pdftocairo'):
                map_dict = {i: '-{}'.format(i) for i in
                            ['png', 'pdf', 'ps', 'eps', 'jpeg', 'svg']}

                outflag = map_dict[outputformat]

                if outputformat in ['png', 'jpeg']:
                    # png jpeg outputname without ext
                    subprocess.check_call(
                        ['pdftocairo', outflag, '-singlefile', '-r', str(dpi),
                         inputimg, output_imgname])

                    if 'win32' == sys.platform.lower():
                        if pdftocairo_fix_encoding:
                            output_imgname2 = convert_encoding(output_imgname,
                                                               'utf8',
                                                               pdftocairo_fix_encoding)

                            if overwrite:
                                os.replace('{}.{}'.format(output_imgname2,
                                                          outputformat),
                                           '{}.{}'.format(output_imgname,
                                                          outputformat))
                            else:
                                try:
                                    os.rename('{}.{}'.format(output_imgname2,
                                                             outputformat),
                                              '{}.{}'.format(output_imgname,
                                                             outputformat))
                                except FileExistsError as e:
                                    click.echo(
                                        'FileExists , i will do nothing.')
                                    os.remove('{}.{}'.format(output_imgname2,
                                                             outputformat))

                else:
                    subprocess.check_call(
                        ['pdftocairo', outflag, '-r', str(dpi), inputimg,
                         outputname])
                return outputimg  # only retcode is zero
            else:
                raise CommandNotFound
        except CommandNotFound as e:
            click.echo('pdftocairo commond not found.', err=True)
        finally:
            os.chdir(currdir)


@click.command()
@click.argument('inputimgs', type=click.Path(), nargs=-1, required=True)
@click.option('--dpi', default=150, type=int, help="the output image dpi")
@click.option('--format', default="png", help="the output image format")
@click.option('--outputdir', default="", help="the image output dir")
@click.option('--outputname', default="", help="the image output name")
@click.option('--pdftocairo-fix-encoding', default="",
              help="In Windows,the pdftocairo fix encoding")
@click.option('--overwrite', default=True,
              help='if output file exist, will be overwrite it?')
def main(inputimgs, dpi, format, outputdir, outputname,
         pdftocairo_fix_encoding, overwrite):
    """
    support image format: \n
      - pillow : png jpg gif eps tiff bmp ppm \n
      - inkscape: svg ->pdf  png ps eps \n
      - pdftocairo: pdf ->  png jpeg ps eps svg\n
    """

    for inputimg in inputimgs:
        outputimg = convert_image(inputimg, outputformat=format, dpi=dpi,
                                  outputdir=outputdir, outputname=outputname,
                                  pdftocairo_fix_encoding=pdftocairo_fix_encoding,
                                  overwrite=overwrite)

        if outputimg:
            click.echo("process: {} done.".format(inputimg))
        else:
            click.echo("process: {} failed.".format(inputimg))


if __name__ == '__main__':
    main()
