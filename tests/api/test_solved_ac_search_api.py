import pytest
from boj.api.solved_ac_search_api import SolvedAcSearchApiParam


@pytest.mark.parametrize(
    "test_in, expected",
    [
        (
            SolvedAcSearchApiParam(
                tags=["dp", "math", "geometry"], lang="ko", tier="g1..g5", user="user1"
            ),
            "tier:g1..g5 -solved_by:user1 lang:ko (tag:dp | tag:math | tag:geometry)",
        ),
        (
            SolvedAcSearchApiParam(
                tags=["dp", "math"], lang="en", tier="s2..s3", user="user2"
            ),
            "tier:s2..s3 -solved_by:user2 lang:en (tag:dp | tag:math)",
        ),
    ],
)
def test_solved_ac_search_api_param(test_in, expected):
    assert test_in.to_query_string() == expected
