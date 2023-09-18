from boj.core.error import ParsingConfigError
from boj.core import util


class LoginOption:
    def __init__(self):
        pass


class InitOption:
    def __init__(self):
        pass


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

    def of_filetype(self, filetype) -> FiletypeConfig:
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
    config.command.run = RunOption(
        verbose=f["command"].get("run", {}).get("verbose", False),
        timeout=f["command"].get("run", {}).get("timeout", 15),
    )

    config.command.submit = SubmitOption(
        verbose=f["command"].get("submit", {}).get("verbose", False),
        timeout=f["command"].get("submit", {}).get("timeout", 15),
        open=f["command"].get("submit", {}).get("open", "onlyaccepted"),
    )

    config.command.random = RandomOption(
        tier=f["command"].get("random", {}).get("tier", None),
        tags=f["command"].get("random", {}).get("tags", []),
    )

    for k, v in f["filetype"].items():
        config.filetype[k] = FiletypeConfig(
            default_language=v.get("default_language", None),
            compile_command=v.get("compile", None),
            run_command=v.get("run", None),
        )

    return config
