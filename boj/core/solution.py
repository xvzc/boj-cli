class Solution:
    def __init__(self, problem_id, filetype, source):
        self.id = problem_id
        self.filetype = filetype 
        self.source = source

    def __repr__(self):
        return (
            "Problem {" + str(self.id) + ", " + self.filetype + ", " + self.source + "}"
        )
