#!/usr/bin/env python
# -*-coding:utf-8-*-

import logging
import click
from ximage import __version__

from ximage.resize_image import resize_image
from ximage.convert_image import convert_image


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('ximage version {}'.format(__version__))
    ctx.exit()


def enable_debug(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    logging.basicConfig(level=logging.DEBUG)


@click.group()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True,
              help="print this software version")
@click.option('-V', '--verbose', is_flag=True, is_eager=True,
              callback=enable_debug, expose_value=False,
              help='print verbose info')
def main():
    """
    ximage --version
    """
    pass


@main.command()
@click.option('-V', '--verbose', is_flag=True, is_eager=True,
              callback=enable_debug, expose_value=False,
              help='print verbose info')
@click.argument('inputimgs', type=click.Path(), nargs=-1, required=True)
@click.option('--width', default=0, type=int, help="the output image width")
@click.option('--height', default=0, help="the output image height")
@click.option('--outputdir', default="", help="the image output dir")
@click.option('--outputname', default="", help="the image output name")
def resize(inputimgs, width, height, outputdir, outputname):
    """
    resize your image, width height you must give one default is zero.
    """

    for inputimg in inputimgs:
        outputimg = resize_image(inputimg, width=width, height=height,
                                 outputdir=outputdir, outputname=outputname)

        if outputimg:
            click.echo("process: {} done.".format(inputimg))
        else:
            click.echo("process: {} failed.".format(inputimg))


@main.command()
@click.option('-V', '--verbose', is_flag=True, is_eager=True,
              callback=enable_debug, expose_value=False,
              help='print verbose info')
@click.argument('inputimgs', type=click.Path(), nargs=-1, required=True)
@click.option('--dpi', default=150, type=int, help="the output image dpi")
@click.option('--format', default="png", help="the output image format")
@click.option('--outputdir', default="", help="the image output dir")
@click.option('--outputname', default="", help="the image output name")
@click.option('--pdftocairo-fix-encoding', default="",
              help="In Windows,the pdftocairo fix encoding")
@click.option('--overwrite/--no-overwrite', default=True,
              help='overwrite the output image file, default is overwrite')
@click.option('--transparent', is_flag=True,
              help="pdf convert to png|tiff can turn transparent on")
def convert(inputimgs, dpi, format, outputdir, outputname,
            pdftocairo_fix_encoding, overwrite, transparent=False):
    """
    support image format: \n
      - pillow : png <-> jpg <-> gif <-> eps <-> tiff <-> bmp <-> ppm \n
      - inkscape: svg -> pdf | png | ps | eps \n
      - pdftocairo: pdf -> png | jpeg | ps | eps | svg \n
    """
    for inputimg in inputimgs:
        outputimg = convert_image(inputimg, outputformat=format, dpi=dpi,
                                  outputdir=outputdir, outputname=outputname,
                                  pdftocairo_fix_encoding=pdftocairo_fix_encoding,
                                  overwrite=overwrite, transparent=transparent)

        if outputimg:
            click.echo("process: {} done.".format(inputimg))
        else:
            click.echo("process: {} failed.".format(inputimg))


if __name__ == '__main__':
    main()
