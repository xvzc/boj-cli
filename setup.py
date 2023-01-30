from setuptools import setup
import re

setup(
    entry_points={
        "console_scripts": ["boj=boj.main:entry"],
    },
    version='0.0.2',
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
        "msgpack==1.0.4",
        "pycparser==2.21",
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
