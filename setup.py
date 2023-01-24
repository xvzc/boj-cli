from setuptools import setup
setup(
    entry_points = {
        'console_scripts': ['boj=boj.main:entry'],
    },
    name='boj-cli',
)

