import os

from setuptools import setup

if "BOJ_CLI_NEXT_VERSION" in os.environ:
    cur_version: str = os.environ["BOJ_CLI_NEXT_VERSION"].replace("v", "")
else:
    cur_version = "0.0.0"

setup(version=cur_version)
