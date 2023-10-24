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
    "label, data_in, data_out",
    [
        ("TestLabel1", "TestDataIn1", "TestDataOut1"),
        ("TestLabel2", "TestDataIn2", "TestDataOut2"),
        ("TestLabel3", "TestDataIn3", "TestDataOut3"),
        ("TestLabel4", "TestDataIn4", "TestDataOut4"),
    ],
)
def test_testcase(label, data_in, data_out):
    testcase = Testcase(label=label, data_in=data_in, data_out=data_out)
    assert testcase.label == label
    assert testcase.data_in == data_in
    assert testcase.data_out == data_out
