import json


class Solution:
    def __init__(self, problem_id, filetype, source):
        self.id = problem_id
        self.filetype = filetype
        self.source = source

    def __repr__(self):
        return (
            "Problem {" + str(self.id) + ", " + self.filetype + ", " + self.source + "}"
        )

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.filetype == other.filetype
            and self.source == other.source
        )


class Testcase:
    __test__ = False
    data_in: str
    data_out: str

    def __init__(self, data_in, data_out):
        self.data_in = data_in
        self.data_out = data_out

    def __repr__(self):
        return "Testcase {" + str(self.data_in) + ", " + self.data_out + "}"


class Credential:
    username: str
    token: str

    def __init__(self, username, token):
        self.username = username
        self.token = token

    def __repr__(self):
        return "Credential {" + str(self.username) + ", " + self.token + "}"

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __eq__(self, other):
        return self.username == other.username and self.token == other.token

    def session_cookies_of(self, online_judge_token):
        return {"bojautologin": self.token, "OnlineJudge": online_judge_token}
