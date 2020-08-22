#!/usr/bin/env python
# -*-coding:utf-8-*-


import pytest
import os
import tempfile
import shutil


@pytest.fixture
def tempfolder():
    cwd = os.getcwd()
    t = tempfile.mkdtemp()

    shutil.copytree(os.path.join(cwd, 'tests/test_images'),
                    os.path.join(t, 'test_images'))

    os.chdir(t)
    try:
        print(f'pytest auto-create tempfolder {t}')
        yield t
    finally:
        os.chdir(cwd)
        try:
            shutil.rmtree(t)
        except (OSError, IOError):  # noqa: B014
            pass
