#!/usr/bin/env python
# -*-coding:utf-8-*-

import logging
import os
import errno
import os.path

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


def detect_output_file_exist(basedir, imgname, outputformat, overwrite):
    filename = '{}.{}'.format(imgname, outputformat)
    filename = os.path.join(basedir, filename)

    if os.path.exists(filename) and not overwrite:
        click.echo('output image file exists. i will give it up.')
        return None
    return filename


def convert_encoding(origin_s, origin_encoding, to_encoding,
                     errors='ignore'):
    b = origin_s.encode(origin_encoding, errors=errors)
    s = b.decode(to_encoding, errors)
    return s
