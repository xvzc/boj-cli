import pytest
from boj.core import util
from boj.core import config
from boj.core.config import DefaultConfig
from boj.core.error import ParsingConfigError


def test_load_default_config(mocker):
    mocker.patch("boj.core.util.read_config_file", return_value={})
    conf = config.load()
    assert conf.command.run.verbose == DefaultConfig.Run.verbose.value
    assert conf.command.run.timeout == DefaultConfig.Run.timeout.value
    assert conf.command.submit.verbose == DefaultConfig.Submit.verbose.value
    assert conf.command.submit.timeout == DefaultConfig.Submit.timeout.value
    assert conf.command.submit.open == DefaultConfig.Submit.open.value
    assert conf.command.random.tier == DefaultConfig.Random.tier.value
    assert conf.command.random.tags == DefaultConfig.Random.tags.value


@pytest.mark.parametrize(
    "test_conf",
    [
        (util.read_yaml("tests/assets/config/test_command_config.yaml")),
    ],
)
def test_load_full_config(test_conf, mocker):
    mocker.patch("boj.core.util.read_config_file", return_value=test_conf)
    conf = config.load()
    assert conf.command.run.verbose == test_conf["command"]["run"]["verbose"]
    assert conf.command.run.timeout == test_conf["command"]["run"]["timeout"]
    assert conf.command.submit.verbose == test_conf["command"]["submit"]["verbose"]
    assert conf.command.submit.timeout == test_conf["command"]["submit"]["timeout"]
    assert conf.command.submit.open == test_conf["command"]["submit"]["open"]
    assert conf.command.random.tier == test_conf["command"]["random"]["tier"]
    assert conf.command.random.tags == test_conf["command"]["random"]["tags"]


@pytest.mark.parametrize(
    "test_conf",
    [
        (util.read_yaml("tests/assets/config/test_filetype_config.yaml")),
    ],
)
def test_filetype_config(test_conf, mocker):
    mocker.patch("boj.core.util.read_config_file", return_value=test_conf)
    conf = config.load()
    filetype_conf = conf.filetype_config_of("cpp")
    assert (
        filetype_conf.default_language
        == test_conf["filetype"]["cpp"]["default_language"]
    )
    assert filetype_conf.compile == test_conf["filetype"]["cpp"]["compile"]
    assert filetype_conf.run == test_conf["filetype"]["cpp"]["run"]


@pytest.mark.parametrize(
    "test_conf",
    [
        (util.read_yaml("tests/assets/config/test_filetype_config_no_language.yaml")),
        (util.read_yaml("tests/assets/config/test_filetype_config_no_run.yaml")),
    ],
)
def test_filetype_config_throws_error(test_conf, mocker):
    mocker.patch("boj.core.util.read_config_file", return_value=test_conf)
    conf = config.load()
    with pytest.raises(ParsingConfigError) as e:
        conf.filetype_config_of("cpp")

    assert e.type == ParsingConfigError
