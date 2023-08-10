from setuptools import setup
import os
import version

latest_version = version.get_latest_version('boj-cli')
if "BOJ_CLI_NEXT_VERSION" in os.environ:
    cur_version: str = os.environ['BOJ_CLI_NEXT_VERSION'][1:]
else:
    cur_version= str(latest_version)

setup(
    long_description='Command line interface for BOJ',
    entry_points={
        "console_scripts": ["boj=boj.main:entry"],
    },
    version=cur_version,
    name="boj-cli",
    author="xvzc",
    url="https://github.com/xvzc/boj-cli",
    install_requires=[
        "beautifulsoup4==4.11.1",
        "certifi==2022.12.7",
        "cffi==1.15.1",
        "charset-normalizer==3.0.1",
        "cryptography==39.0.0",
        "greenlet==2.0.1",
        "idna==3.4",
        "mdurl==0.1.2",
        "selenium==4.11.2",
        "msgpack==1.0.4",
        "pycparser==2.21",
        "chromedriver-autoinstaller==0.6.2",
        "Pygments==2.14.0",
        "requests==2.28.2",
        "rich==13.2.0",
        "six==1.16.0",
        "soupsieve==2.3.2.post1",
        "urllib3==1.26.14",
        "websockets==10.4",
        "PyYAML==6.0",
    ],
)
