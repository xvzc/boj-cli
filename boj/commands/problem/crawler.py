from bs4 import BeautifulSoup
import requests, re
import boj.core.util as util
import markdownify


# Returns markdown
def query_problem(problem_id):
    res = requests.get(util.problem_url(problem_id), headers=util.headers())
    return res.text

def markdownify_problem(html, problem_id):
    soup = BeautifulSoup(html, "html.parser")

    problem_sections = soup.select("#problem-body > div")[:-1]

    problem_html = ""
    for div in problem_sections:
        problem_html += str(div) + "\n"

    ## Prettify
    problem_html = re.sub(r"<button.+\n", "", problem_html)
    problem_html = re.sub(r"h2", "h1", problem_html)
    problem_html += "LINK: " + util.problem_url(problem_id) + "\n"

    return markdownify.markdownify(problem_html)
