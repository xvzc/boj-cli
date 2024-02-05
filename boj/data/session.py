class Session:
    def __init__(self, credential, cookies):
        self.__credential = credential
        self.__online_judge = cookies["OnlineJudge"]

    @property
    def credential(self):
        return self.__credential

    @property
    def online_judge(self):
        return self.__online_judge

    @property
    def session_cookies(self) -> dict:
        return {
            "bojautologin": self.credential.token,
            "OnlineJudge": self.online_judge,
        }

    def __repr__(self):
        return "Session { " + str(self.__credential) + ", " + self.online_judge + " }"
