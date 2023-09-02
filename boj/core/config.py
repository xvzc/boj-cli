class CommandOption:
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

    class SubmitOption:
        verbose: bool
        timeout: int

        def __init__(self, verbose, timeout):
            self.verbose = verbose
            self.timeout = timeout

    class RandomOption:
        tier: str
        tags: list[str]

        def __init__(self, tier, tags):
            self.tier = tier
            self.tags = tags

    login: LoginOption
    init: InitOption
    open: OpenOption
    run: RunOption
    submit: SubmitOption
    random: RandomOption


class FiletypeConfig:
    default_language: str
    compile: str
    run: str

    def __init__(self, default_language, compile_command, run_command):
        self.default_language = default_language
        self.compile = compile_command
        self.run = run_command


class Config:
    command: CommandOption
    filetype: dict[str, FiletypeConfig]
