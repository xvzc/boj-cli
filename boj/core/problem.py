class Problem:
    id: str
    filetype: str
    source: str

    def __init__(self, id, language, source):
        self.id = id
        self.filetype = language
        self.source = source

    def __repr__(self):
        return (
            "Problem {" + str(self.id) + ", " + self.filetype + ", " + self.source + "}"
        )
