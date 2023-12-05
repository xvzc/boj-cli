import json


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
