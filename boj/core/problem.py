class Problem:
    id: str
    filetype: str
    source: str

    def __init__(self, id, filetype, source):
        self.id = id
        self.filetype = filetype 
        self.source = source

    def __repr__(self):
        return (
            "Problem {" + str(self.id) + ", " + self.filetype + ", " + self.source + "}"
        )
