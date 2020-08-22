#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

from PIL import Image
import click

from ximage.utils import mkdirs

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)


def resize_image(inputimg, width=0, height=0, outputdir='', outputname=''):
    """
    width and height if you only specify one parameter of them, then the another will dismissed.
    if you given a overhigh height, then there maybe output a image not resize at all.
    """
    imgname, imgext = os.path.splitext(os.path.basename(inputimg))

    if not os.path.exists(os.path.abspath(outputdir)):
        mkdirs(outputdir)

    if not outputname:
        outputname = imgname + '_resized' + imgext
    else:
        output_imgname, ext = os.path.splitext(outputname)
        if not ext:
            outputname = output_imgname + '_resized' + imgext
        elif ext != imgext:
            raise Exception(
                'outputname ext is not the same as the intput image')

    try:
        im = Image.open(os.path.abspath(inputimg))
        ori_w, ori_h = im.size

        if width is 0 and height is not 0:  # given height and make width meanful
            width = ori_w
        elif width is not 0 and height is 0:
            height = ori_h
        elif width is 0 and height is 0:
            click.echo('you must give one value , height or width', err=True)
            raise IOError

        if width > ori_w:
            logger.warning(
                'the target width is larger than origin, i will use the origin one')
            width = ori_w
        elif height > ori_h:
            logger.warning(
                'the target height is larger than origin, i will use the origin one')
            height = ori_h

        logger.debug(f'pillow resize target ({width},{height})')
        im.thumbnail((width, height), Image.ANTIALIAS)

        logger.info(os.path.abspath(inputimg))

        outputimg = os.path.join(os.path.abspath(outputdir), outputname)

        logger.debug(f'pillow resize output image to {outputimg}')
        im.save(outputimg)
        click.echo('{0} saved.'.format(outputimg))
        return outputimg
    except IOError:
        logging.error('IOError, I can not resize {}'.format(inputimg))
