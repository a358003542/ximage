#!/usr/bin/env python
# -*-coding:utf-8-*-


from click.testing import CliRunner
from ximage.__main__ import main


def test_main_command():
    runner = CliRunner()
    result = runner.invoke(main)

    assert result.exit_code == 0

    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0
