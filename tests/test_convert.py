#!/usr/bin/env python
# -*-coding:utf-8-*-


from click.testing import CliRunner
from ximage.__main__ import main


def test_convert_command(tempfolder):
    runner = CliRunner()

    result = runner.invoke(main,
                           ['convert','test_images/中文.pdf', '-V'])

    assert result.exit_code == 0
    assert 'done' in result.output


def test_multi_folder_convert_command(tempfolder):
    runner = CliRunner()

    result = runner.invoke(main,
                           ['convert','--outputdir', 'other_folder',
                            'test_images/other_folder/中文2.pdf', '-V'])
    assert result.exit_code == 0
    assert 'done' in result.output
    result = runner.invoke(main,
                           ['convert','--outputdir', 'other_folder',
                            'test_images/other_folder/中文3.pdf', '-V'])
    assert result.exit_code == 0
    assert 'done' in result.output
    result = runner.invoke(main,
                           ['convert','--outputdir', 'other_folder/other_folder2',
                            'test_images/other_folder/other_folder2/中文4.pdf',
                            '-V'])
    assert result.exit_code == 0
    assert 'done' in result.output
    result = runner.invoke(main,
                           ['convert', '--outputdir', 'other_folder/other_folder2',
                            'test_images/other_folder/other_folder2/中文5.pdf',
                            '-V'])
    assert result.exit_code == 0
    assert 'done' in result.output
