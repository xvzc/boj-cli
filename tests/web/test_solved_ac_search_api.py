import pytest

from boj.web.solved_ac_search_api import make_solved_ac_search_api_params


@pytest.mark.parametrize(
    "actual, expected",
    [
        (
            make_solved_ac_search_api_params(
                tags=["dp", "geometry"],
                lang="ko",
                tier="g1..g5",
                user="user1",
            ),
            dict(
                query="tier:g1..g5 -solved_by:user1 lang:ko (tag:dp | tag:geometry)",
                page=1,
                sort="random",
                direction="asc",
            ),
        ),
        (
            make_solved_ac_search_api_params(
                tags=["dp", "geometry"],
                lang="ko",
                tier="g1..g5",
                user="user1",
                page=2,
            ),
            dict(
                query="tier:g1..g5 -solved_by:user1 lang:ko (tag:dp | tag:geometry)",
                page=2,
                sort="random",
                direction="asc",
            ),
        ),
        (
            make_solved_ac_search_api_params(
                tags=["dp", "geometry"],
                lang="ko",
                tier="g1..g5",
                user="user1",
                direction="desc",
                page=3,
            ),
            dict(
                query="tier:g1..g5 -solved_by:user1 lang:ko (tag:dp | tag:geometry)",
                page=3,
                sort="random",
                direction="desc",
            ),
        ),
    ],
)
def test_make_solved_ac_search_api_params(actual, expected):
    assert actual == expected
