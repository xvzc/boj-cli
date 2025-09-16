import re
from typing import Optional, Dict, Any

from bs4 import BeautifulSoup

from boj.core import constant
from boj.core.html import HtmlParser
from boj.core.http import RequestWithParams
from boj.data.testcase import Testcase


class BojProblemPageRequest(RequestWithParams):
    def __init__(self, problem_id: str):
        self.__problem_id = problem_id

    def url(self) -> str:
        return constant.boj_problem_url(self.__problem_id)

    def headers(self) -> Optional[dict]:
        return constant.default_headers()

    def cookies(self) -> Optional[dict]:
        return None

    def params(self) -> Optional[dict]:
        return None


class TitleParser(HtmlParser[str]):
    def find(self, html) -> str:
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find("span", id="problem_title")
        return title.text


class TestcaseParser(HtmlParser[list[Testcase]]):
    def find(self, html) -> list[Testcase]:
        soup = BeautifulSoup(html, "html.parser")
        sample_data = soup.select("pre.sampledata")

        inputs = []
        outputs = []
        for data in sample_data:
            text = data.text

            if "input" in str(data.get("id", "")):
                inputs.append(text)

            if "output" in str(data.get("id", "")):
                outputs.append(text)

        test_idx = 1
        testcases: list[Testcase] = []
        for data_in, data_out in zip(inputs, outputs):
            testcases.append(
                Testcase(label=str(test_idx), input_=data_in, output=data_out)
            )

            test_idx += 1

        return testcases


class ProblemInfoParser(HtmlParser[Dict[str, Any]]):
    def find(self, html) -> Dict[str, Any]:
        soup = BeautifulSoup(html, "html.parser")

        # Problem title
        title_element = soup.find("span", id="problem_title")
        title = title_element.text.strip() if title_element else "Unknown Title"

        # Problem number
        problem_id = self._extract_problem_id(soup)

        # Time limit and memory limit
        time_limit, memory_limit = self._extract_limits(soup)

        # Process problem description, input description, and output description at once
        descriptions = self._extract_descriptions(soup)

        return {
            "problem_id": problem_id,
            "title": title,
            "time_limit": time_limit,
            "memory_limit": memory_limit,
            "description": descriptions["problem"],
            "input_description": descriptions["input"],
            "output_description": descriptions["output"],
        }

    def _extract_problem_id(self, soup: BeautifulSoup) -> str:
        h1_element = soup.find("h1")
        if h1_element:
            text = h1_element.get_text()
            match = re.search(r"(\d+)번", text)
            if match:
                return match.group(1)

        return "Unknown"

    def _extract_limits(self, soup: BeautifulSoup) -> tuple[str, str]:
        time_limit = "Unknown"
        memory_limit = "Unknown"

        table = soup.find("table", id="problem-info")
        if table:
            tbody = table.find("tbody")
            if tbody:
                row = tbody.find("tr")
                if row:
                    cells = row.find_all("td")
                    if len(cells) >= 2:
                        time_limit = cells[0].get_text().strip()
                        memory_limit = cells[1].get_text().strip()

        return time_limit, memory_limit

    def _extract_descriptions(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract problem description, input description, and output description"""
        descriptions = {"problem": "", "input": "", "output": ""}

        # Find and process each description section
        section_ids = {
            "problem": "problem_description",
            "input": "problem_input",
            "output": "problem_output",
        }

        for key, section_id in section_ids.items():
            element = soup.find("div", id=section_id)
            if element:
                descriptions[key] = self._clean_html_text(element)

        return descriptions

    def _clean_html_text(self, element) -> str:
        """Convert HTML elements to markdown and extract text"""
        if not element:
            return ""

        # Parse with BeautifulSoup
        soup = BeautifulSoup(str(element), "html.parser")

        # Convert HTML tags to markdown
        self._convert_html_to_markdown(soup)

        # Extract and clean text
        text = soup.get_text()
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
        text = re.sub(r"([^\n])\n([^\n#\-\*\d])", r"\1  \n\2", text)

        return text.strip()

    def _convert_html_to_markdown(self, soup: BeautifulSoup) -> None:
        """Convert HTML tags to markdown"""

        # Convert images
        for img in soup.find_all("img"):
            self._convert_image(img)

        # Convert code blocks
        for pre in soup.find_all("pre"):
            self._convert_pre(pre)

        # Convert inline code
        for code in soup.find_all("code"):
            self._convert_inline_code(code)

        # Convert bold text
        for strong in soup.find_all(["strong", "b"]):
            self._convert_emphasis(strong, "**")

        for em in soup.find_all(["em", "i"]):
            self._convert_emphasis(em, "*")

        # Convert links
        for a in soup.find_all("a"):
            self._convert_link(a)

        # Convert lists
        for ul in soup.find_all("ul"):
            self._convert_list(ul, "-")

        for ol in soup.find_all("ol"):
            self._convert_list(ol, "1.")

        # Convert headings
        for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
            self._convert_heading(heading)

        # Convert blockquotes
        for blockquote in soup.find_all("blockquote"):
            self._convert_blockquote(blockquote)

        # Convert horizontal rules
        for hr in soup.find_all("hr"):
            hr.replace_with("\n---\n")

        # Convert line breaks
        for br in soup.find_all("br"):
            br.replace_with("\n")

    def _convert_image(self, element) -> None:
        """Convert image tags to markdown"""
        src = element.get("src", "")
        alt = element.get("alt", "")

        if src:
            # Convert relative path to absolute path
            if not src.startswith(("http://", "https://")):
                src = f"https://www.acmicpc.net{src}"

            img_markdown = f"![{alt or '이미지'}]({src})"
            element.replace_with(img_markdown)

    def _convert_pre(self, element) -> None:
        """Convert pre tags to code blocks"""
        for code in element.find_all("code"):
            code_text = code.get_text()
            code.replace_with(code_text)

        # Get text content from pre tag and convert to code block
        pre_text = element.get_text()
        pre_text = re.sub(r"\n\s*\n\s*\n+", "\n\n", pre_text)
        pre_text = pre_text.strip()
        element.replace_with(f"```\n{pre_text}\n```")

    def _convert_inline_code(self, element) -> None:
        """Convert inline code to markdown (only code outside pre tags)"""
        if not element.find_parent("pre"):
            code_text = element.get_text()
            element.replace_with(f"`{code_text}`")

    def _convert_emphasis(self, element, marker: str) -> None:
        """Convert emphasis text to markdown"""
        text = element.get_text()
        element.replace_with(f"{marker}{text}{marker}")

    def _convert_link(self, element) -> None:
        """Convert links to markdown"""
        href = element.get("href", "")
        text = element.get_text()
        if href:
            element.replace_with(f"[{text}]({href})")

    def _convert_list(self, element, marker: str) -> None:
        """Convert lists to markdown"""
        items = element.find_all("li", recursive=False)

        list_items = []
        for i, item in enumerate(items):
            text = item.get_text().strip()
            if marker == "1.":
                list_items.append(f"{i + 1}. {text}")
            else:
                list_items.append(f"{marker} {text}")

        # Join list items with line breaks (add empty line at the end)
        element.replace_with("\n".join(list_items) + "\n")

    def _convert_heading(self, element) -> None:
        """Convert headings to markdown"""
        level = int(element.name[1])
        text = element.get_text().strip()
        element.replace_with(f"{'#' * level} {text}\n")

    def _convert_blockquote(self, element) -> None:
        """Convert blockquotes to markdown"""
        text = element.get_text()
        lines = text.split("\n")
        quoted_lines = [f"> {line.strip()}" for line in lines if line.strip()]
        element.replace_with("\n".join(quoted_lines) + "\n")


def generate_readme(problem_info: Dict[str, Any]) -> str:
    """Generate README.md content based on problem information"""
    sections = []

    # Header
    sections.append(f"# {problem_info['problem_id']}. {problem_info['title']}")
    sections.append("")

    # Problem information
    sections.append("## Problem information")
    sections.extend(
        [
            f"- **Problem number**: {problem_info['problem_id']}",
            f"- **Title**: {problem_info['title']}",
            f"- **Time limit**: {problem_info['time_limit']}",
            f"- **Memory limit**: {problem_info['memory_limit']}",
            "",
        ]
    )

    # Description sections
    description_sections = [
        ("description", "Problem description"),
        ("input_description", "Input"),
        ("output_description", "Output"),
    ]

    for key, title in description_sections:
        if problem_info.get(key):
            sections.extend([f"## {title}", problem_info[key], ""])

    # Links
    sections.extend(
        [
            "## Links",
            f"- [BOJ {problem_info['problem_id']}](https://www.acmicpc.net/problem/{problem_info['problem_id']})",
            "",
        ]
    )

    return "\n".join(sections)
