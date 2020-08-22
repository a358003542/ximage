#!/usr/bin/env python
# -*-coding:utf-8-*-

import os
from click.testing import CliRunner
from ximage.__main__ import main


def test_resize_command(tempfolder):
    runner = CliRunner()

    result = runner.invoke(main, ['resize', '--width', '30',
                                  'test_images/test.png', '-V'])

    assert result.exit_code == 0
    assert 'done' in result.output
