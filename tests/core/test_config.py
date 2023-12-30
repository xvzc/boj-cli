from os.path import abspath, join
from os.path import dirname as d


import pytest
from boj.core import util
from boj.core.config import Config
from boj.core.error import ParsingConfigError


@pytest.mark.parametrize(
    "conf_name",
    [
        "test_filetype_config.yaml",
    ],
)
def test_filetype_config(request, conf_name):
    rootdir = request.config.rootdir
    conf = Config.load(
        suffix="test_filetype_config.yaml",
        cwd=join(rootdir, "tests", "assets", "config"),
    )

    test_conf = util.read_yaml(join(rootdir, "tests", "assets", "config", conf_name))

    filetype_conf = conf.of_filetype("cpp")
    assert filetype_conf.language == test_conf["filetype"]["cpp"]["language"]
    assert filetype_conf.compile == test_conf["filetype"]["cpp"]["compile"]
    assert filetype_conf.run == test_conf["filetype"]["cpp"]["run"]


@pytest.mark.parametrize(
    ("conf_name"),
    [
        "test_filetype_no_lang_config.yaml",
        "test_filetype_no_run_config.yaml",
    ],
)
def test_filetype_config_throws_error(request, conf_name):
    rootdir = request.config.rootdir
    conf = Config.load(
        suffix=conf_name,
        cwd=join(rootdir, "tests", "assets", "config"),
    )

    with pytest.raises(ParsingConfigError) as e:
        conf.of_filetype("cpp")

    assert e.type == ParsingConfigError


def test_ini(request):
    print(request.config.rootdir)
    print(request.config.rootdir)
    print(request.config.rootdir)
    print(request.config.rootdir)
    print(request.config.rootdir)
    print(request.config.rootdir)
    print(request.config.rootdir)
    assert True
