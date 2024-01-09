import os.path

import pytest

from boj.core.error import IllegalStatementError
from boj.data.boj_info import BojInfo


def test_read(request):
    rootdir = request.config.rootdir
    info = BojInfo.read(
        problem_root=os.path.join(rootdir, "tests", "assets", "boj-info")
    )
    assert info.id == 1010


def test_find_any_with_backtrace(request):
    rootdir = request.config.rootdir
    info = BojInfo.find_any(
        problem_dir="",
        problem_id="",
        cwd=os.path.join(rootdir, "tests", "assets", "boj-info"),
    )
    assert info.id == 1010


def test_find_any_with_read(request):
    rootdir = request.config.rootdir
    info = BojInfo.find_any(
        problem_dir=os.path.join(rootdir, "tests", "assets"),
        problem_id="boj-info",
    )
    assert info.id == 1010


@pytest.mark.parametrize(
    "problem_dir, problem_id, error",
    [
        (os.path.join(os.getcwd(), "INVALID_DIR"), "", IllegalStatementError),
        (os.path.join(os.getcwd(), "INVALID_DIR"), "1234", IllegalStatementError),
    ],
)
def test_find_any_throw_error(problem_dir, problem_id, error):
    with pytest.raises(IllegalStatementError) as e:
        BojInfo.find_any(
            problem_dir=problem_dir,
            problem_id=problem_id,
        )

    assert e.type == error
