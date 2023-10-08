from boj.core.data import Solution
from boj.core.data import Testcase
import pytest


@pytest.mark.parametrize(
    "problem_id, filetype, source",
    [
        (1234, "cpp", "TestSourceCode 1234"),
        (1000, "cpp", "TestSourceCode 1000"),
        (1649, "cpp", "TestSourceCode 1649"),
        (3455, "cpp", "TestSourceCode 3455"),
    ],
)
def test_solution(problem_id, filetype, source):
    solution = Solution(problem_id=problem_id, filetype=filetype, source=source)

    assert solution.id == problem_id
    assert solution.filetype == filetype
    assert solution.source == source


@pytest.mark.parametrize(
    "data_in, data_out",
    [
        ("TestDataIn1", "TestDataOut1"),
        ("TestDataIn2", "TestDataOut2"),
        ("TestDataIn3", "TestDataOut3"),
        ("TestDataIn4", "TestDataOut4"),
    ],
)
def test_testcase(data_in, data_out):
    testcase = Testcase(data_in=data_in, data_out=data_out)
    assert testcase.data_in == data_in
    assert testcase.data_out == data_out
