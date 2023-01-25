from bs4 import BeautifulSoup
import requests, re
import boj.core.util as util
import markdownify


# Returns markdown
def query_problem(problem_id):
    res = requests.get(util.problem_url(problem_id), headers=util.headers())

    soup = BeautifulSoup(res.text, "html.parser")

    problem_sections = soup.select("#problem-body > div")[:-1]

    html = ""
    for div in problem_sections:
        html += str(div) + "\n"

    ## Prettify
    html = re.sub(r"<button.+\n", "", html)
    html = re.sub(r"h2", "h1", html)
    html += "LINK: " + util.problem_url(problem_id) + "\n"

    return markdownify.markdownify(html)
