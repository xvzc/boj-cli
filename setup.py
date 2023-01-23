from setuptools import setup
setup(
    entry_points = {
        'console_scripts': ['boj=boj.cli:run'],
    },
    name='boj-cli',
)
