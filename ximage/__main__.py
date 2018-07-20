#!/usr/bin/env python
# -*-coding:utf-8-*-

import click
from ximage import __version__

from ximage.resize.resize_image import resize_image
from ximage.convert.convert_image import convert_image

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version {}'.format(__version__))
    ctx.exit()


@click.group()
@click.option('--version', is_flag=True, callback=print_version,
    expose_value=False, is_eager=True,help="print this software version")
def main():
    """ximage --version
    please remember here what will do if you call the subcommand,so here generally is doing nothing.
    """
    pass



@main.command()
@click.argument('inputimgs',type=click.Path(),nargs=-1,required=True)
@click.option('--width',default=0,type=int,help="the output image width")
@click.option('--height',default=0,help="the output image height")
@click.option('--outputdir',default="",help="the image output dir")
@click.option('--outputname',default="",help="the image output name")
def resize(inputimgs,width,height,outputdir,outputname):
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
        outputimg = resize_image(inputimg,width=width,height=height,outputdir=outputdir,outputname=outputname)

        if outputimg:
            click.echo("process: {} done.".format(inputimg))
        else:
            click.echo("process: {} failed.".format(inputimg))


@main.command()
@click.argument('inputimgs', type=click.Path(), nargs=-1, required=True)
@click.option('--dpi', default=150, type=int, help="the output image dpi")
@click.option('--format', default="png", help="the output image format")
@click.option('--outputdir', default="", help="the image output dir")
@click.option('--outputname', default="", help="the image output name")
def convert(inputimgs, dpi, format, outputdir, outputname):
    """
    support image format: \n
      - pillow : png jpg gif eps tiff bmp ppm \n
      - inkscape: svg ->pdf  png ps eps \n
      - pdftoppm: pdf ->  png \n
      - pdf2svg: pdf ->  svg
    """

    for inputimg in inputimgs:
        outputimg = convert_image(inputimg, outputformat=format, dpi=dpi, outputdir=outputdir, outputname=outputname)

        if outputimg:
            click.echo("process: {} done.".format(inputimg))
        else:
            click.echo("process: {} failed.".format(inputimg))

if __name__ == '__main__':
    main()