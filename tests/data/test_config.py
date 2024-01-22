from os.path import join

import pytest
from boj.core import util
from boj.data.config import Config
from boj.core.error import ParsingConfigError


@pytest.mark.parametrize(
    "conf_name",
    [
        "test_filetype_config.yaml",
    ],
)
def test_filetype_config(request, conf_name):
    root_dir = request.config.rootdir
    conf = Config.load(
        suffix="test_filetype_config.yaml",
        cwd=join(root_dir, "tests", "assets", "config"),
    )

    test_conf = util.read_yaml(join(root_dir, "tests", "assets", "config", conf_name))

    filetype_conf = conf.of_filetype("cpp")
    assert filetype_conf.language == test_conf["filetype"]["cpp"]["language"]
    assert filetype_conf.compile == test_conf["filetype"]["cpp"]["compile"]
    assert filetype_conf.run == test_conf["filetype"]["cpp"]["run"]


@pytest.mark.parametrize(
    "filename",
    [
        "test_filetype_no_lang_config.yaml",
        "test_filetype_no_run_config.yaml",
    ],
)
def test_filetype_config_throws_error(request, filename):
    root_dir = request.config.rootdir
    conf = Config.load(
        suffix=filename,
        cwd=join(root_dir, "tests", "assets", "config"),
    )

    with pytest.raises(ParsingConfigError) as e:
        conf.of_filetype("cpp")

    assert e.type == ParsingConfigError
