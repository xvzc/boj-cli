import os.path

import pytest
from boj.core import util
from boj.core.config import Config
from boj.core.error import ParsingConfigError


@pytest.mark.parametrize(
    "test_conf",
    [
        util.read_yaml(os.path.join("tests", "assets", "config", "test_filetype_config.yaml")),
    ],
)
def test_filetype_config(test_conf):
    conf = Config.load(
        suffix="test_filetype_config.yaml",
        cwd=os.path.join(os.getcwd(), "tests", "assets", "config"),
    )
    filetype_conf = conf.of_filetype("cpp")
    assert filetype_conf.language == test_conf["filetype"]["cpp"]["language"]
    assert filetype_conf.compile == test_conf["filetype"]["cpp"]["compile"]
    assert filetype_conf.run == test_conf["filetype"]["cpp"]["run"]


@pytest.mark.parametrize(
    ("suffix", "test_conf"),
    [
        (
            "test_filetype_no_lang_config.yaml",
            util.read_yaml(os.path.join("tests", "assets", "config", "test_filetype_no_lang_config.yaml")),
        ),
        (
            "test_filetype_no_run_config.yaml",
            util.read_yaml(os.path.join("tests", "assets", "config", "test_filetype_no_run_config.yaml")),
        ),
    ],
)
def test_filetype_config_throws_error(suffix, test_conf):
    conf = Config.load(
        suffix=suffix,
        cwd=os.path.join(os.getcwd(), "tests", "assets", "config"),
    )
    with pytest.raises(ParsingConfigError) as e:
        conf.of_filetype("cpp")

    assert e.type == ParsingConfigError
