#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import os
from PIL import Image
import errno
import click

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


def resize_image(inputimg, width=0, height=0, outputdir='', outputname=''):
    """
    width和height如果只指定一个则另外一个不考虑，如果两个都指定则常规执行。如果给定宽度过高则可能不resize
    :param inputimg:
    :param width:
    :param height:
    :param outputdir:
    :param outputname:
    :return:
    """
    imgname, imgext = os.path.splitext(os.path.basename(inputimg))

    try:
        im = Image.open(os.path.abspath(inputimg))
        ori_w, ori_h = im.size

        if width is 0 and height is not 0:  # given height and make width meanful
            width = ori_w
        elif width is not 0 and height is 0:
            height = ori_h
        elif width is 0 and height is 0:
            logger.error('you must give one value , height or width')
            raise IOError

        if width > ori_w:
            logger.warning('the target width is larger than origin, i will use the origin one')
            width = ori_w
        elif height > ori_h:
            logger.warning('the target height is larger than origin, i will use the origin one')
            height = ori_h

        im.thumbnail((width, height), Image.ANTIALIAS)

        logger.info(os.path.abspath(inputimg))

        if not os.path.exists(os.path.abspath(outputdir)):
            mkdirs(outputdir)
        if not outputname:
            outputname = imgname + '_resized' + imgext

        outputimg = os.path.join(os.path.abspath(outputdir), outputname)

        im.save(outputimg)
        logger.info('{0} saved.'.format(outputimg))
        return outputimg
    except IOError:
        logging.error('IOError, I can not resize {}'.format(inputimg))


@click.command()
@click.argument('inputimgs', type=click.Path(), nargs=-1, required=True)
@click.option('--width', default=0, type=int, help="the output image width")
@click.option('--height', default=0, help="the output image height")
@click.option('--outputdir', default="", help="the image output dir")
@click.option('--outputname', default="", help="the image output name")
def main(inputimgs, width, height, outputdir, outputname):
    """
    resize your image, width height you must give one default is zero.
    out
    :param inputimgs:
    :param width:
    :param height:
    :param outputdir:
    :param outputname:
    :return:
    """

    for inputimg in inputimgs:
        outputimg = resize_image(inputimg, width=width, height=height, outputdir=outputdir, outputname=outputname)

        if outputimg:
            click.echo("process: {} done.".format(inputimg))
        else:
            click.echo("process: {} failed.".format(inputimg))


if __name__ == '__main__':
    main()
