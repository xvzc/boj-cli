import os
import time

from boj.core import http
from boj.core import constant
from boj.core import util
from boj.core.base import Command
from boj.core.error import ParsingConfigError, IllegalStatementError
from boj.core.config import Config, FiletypeConfig
from boj.core.out import BojConsole
from boj.data.template_file import TemplateFile
from boj.data.testcase import TomlTestcase
from boj.pages.boj_problem_page import BojProblemPage
from boj.data.boj_info import BojInfo


class AddCommand(Command):
    def execute(self, args):
        config = Config.load()

        console = BojConsole()
        with console.status("Creating testcases...") as status:
            time.sleep(0.5)

            problem_dir = os.path.join(
                config.workspace.problem_dir, str(args.problem_id)
            )

            if util.file_exists(os.path.join(problem_dir, ".boj-info.json")):
                raise IllegalStatementError(f"Problem {args.problem_id} already exists")

            # Get HTML content of given problem id from BOJ
            response = http.get(
                url=constant.boj_problem_url(args.problem_id),
                headers=constant.default_headers(),
            )

            # Get language config
            filetype_config: FiletypeConfig = config.of_filetype(args.filetype)
            source_dir = config.get_source_dir(
                problem_id=args.problem_id, filetype=args.filetype
            )
            os.makedirs(
                source_dir,
                exist_ok=True,
            )

            # Create testcase file
            problem_page = BojProblemPage(html=response.text)
            toml_testcase = TomlTestcase(problem_page.extract_testcases())
            toml_testcase.save(dir_=source_dir)

            # Create manifest files
            if filetype_config.manifest_files:
                for f in filetype_config.manifest_files:
                    try:
                        manifest = TemplateFile.read_file(
                            path=os.path.join(config.workspace.template_dir, f)
                        )
                        manifest.save(path=os.path.join(problem_dir, f))
                    except (Exception,) as e:
                        console.log(e)

            # Create template file
            file_path = os.path.join(source_dir, filetype_config.filename)
            try:
                template = TemplateFile.read_file(
                    path=os.path.join(
                        config.workspace.template_dir, f"template.{args.filetype}"
                    )
                )
                template.save(path=file_path)
            except (FileNotFoundError,) as e:
                console.log(e)
                util.write_file(
                    file_path,
                    bytes("", "utf-8"),
                )

            # Create BojInfo
            boj_info = BojInfo(
                root_dir=problem_dir,
                id_=args.problem_id,
                title=problem_page.extract_title(),
                filetype=args.filetype,
                language=filetype_config.language,
                source_path=os.path.join(source_dir, filetype_config.filename).replace(
                    os.path.join(problem_dir, ""), ""
                ),
                testcase_path=os.path.join(source_dir, "testcase.toml").replace(
                    os.path.join(problem_dir, ""), ""
                ),
                checksum=util.file_hash(
                    os.path.join(source_dir, filetype_config.filename)
                ),
                accepted=False,
            )
            boj_info.save()
            console.print(f"Successfully initialized the problem {args.problem_id}")
