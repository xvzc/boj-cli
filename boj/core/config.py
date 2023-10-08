from enum import Enum

from boj.core.error import ParsingConfigError
from boj.core import util


class LoginOption:
    def __init__(self):
        pass


class InitOption:
    lang: str

    def __init__(self, lang):
        self.lang = lang


class OpenOption:
    def __init__(self):
        pass


class RunOption:
    verbose: bool
    timeout: int

    def __init__(self, verbose, timeout):
        self.verbose = verbose
        self.timeout = timeout

    def __repr__(self):
        return "RunOption {" + str(self.verbose) + ", " + str(self.timeout) + "}"


class SubmitOption:
    verbose: bool
    timeout: int
    open: str

    def __init__(self, verbose, timeout, open):
        self.verbose = verbose
        self.timeout = timeout
        self.open = open

    def __repr__(self):
        return "SubmitOption {" + str(self.verbose) + ", " + str(self.timeout) + "}"


class RandomOption:
    tier: str
    tags: list[str]

    def __init__(self, tier, tags):
        self.tier = tier
        self.tags = tags

    def __repr__(self):
        return "RandomOption {" + str(self.tier) + ", " + str(self.tags) + "}"


class CommandConfig:
    init: InitOption
    login: LoginOption
    open: OpenOption
    random: RandomOption
    run: RunOption
    submit: SubmitOption


class DefaultConfig:
    class Login(Enum):
        pass

    class Init(Enum):
        lang: str = None

    class Open(Enum):
        pass

    class Random(Enum):
        tier: str = None
        tags: list[str] = []

    class Run(Enum):
        verbose: bool = False
        timeout: int = 15

    class Submit(Enum):
        verbose: bool = False
        timeout: int = 15
        open: str = "onlyaccepted"


class FiletypeConfig:
    default_language: str
    compile: str
    run: str

    def __init__(self, default_language, compile_command, run_command):
        self.default_language = default_language
        self.compile = compile_command
        self.run = run_command


class Config:
    command: CommandConfig
    filetype: dict[str, FiletypeConfig]

    def __init__(self):
        self.command = CommandConfig()
        self.filetype = {}

    def filetype_config_of(self, filetype) -> FiletypeConfig:
        config = self.filetype[filetype]
        if not config.default_language:
            raise ParsingConfigError(
                f"'default_language' option for filetype {filetype} is not found."
            )

        if not config.run:
            raise ParsingConfigError(
                f"'run' option for filetype {filetype} is not found."
            )

        return config


def load() -> Config:
    f = util.read_config_file()
    if "command" not in f:
        f["command"] = {}

    if "filetype" not in f:
        f["filetype"] = {}

    config = Config()
    config.command.init = InitOption(
        lang=f["command"].get("init", {}).get("lang", DefaultConfig.Init.lang.value),
    )

    config.command.run = RunOption(
        verbose=f["command"].get("run", {}).get("verbose", DefaultConfig.Run.verbose.value),
        timeout=f["command"].get("run", {}).get("timeout", DefaultConfig.Run.timeout.value),
    )

    config.command.submit = SubmitOption(
        verbose=f["command"]
        .get("submit", {})
        .get("verbose", DefaultConfig.Submit.verbose.value),
        timeout=f["command"]
        .get("submit", {})
        .get("timeout", DefaultConfig.Submit.timeout.value),
        open=f["command"].get("submit", {}).get("open", DefaultConfig.Submit.open.value),
    )

    config.command.random = RandomOption(
        tier=f["command"].get("random", {}).get("tier", DefaultConfig.Random.tier.value),
        tags=f["command"].get("random", {}).get("tags", DefaultConfig.Random.tags.value),
    )

    for k, v in f["filetype"].items():
        config.filetype[k] = FiletypeConfig(
            default_language=v.get("default_language", None),
            compile_command=v.get("compile", None),
            run_command=v.get("run", None),
        )

    return config
