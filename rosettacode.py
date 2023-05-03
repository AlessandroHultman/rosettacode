import requests
from bs4 import BeautifulSoup


BASE_URL = "https://rosettacode.org/wiki/"


class Category:
    def __init__(self, name):
        self.name = name
        self.url = BASE_URL + name
        self.tasks = []
        self._fetch_tasks()

    def _fetch_tasks(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        task_list = soup.find("div", id="mw-pages")
        if task_list:
            links = task_list.find_all("a")
            for link in links:
                task_name = link.text
                task_url = link["href"]
                self.tasks.append(Task(task_name, task_url))

    def to_json(self):
        return {
            "name": self.name,
            "url": self.url,
            "tasks": [task.to_json() for task in self.tasks],
        }


class Task:
    def __init__(self, name, url=None):
        self.name = name
        self.url = url or BASE_URL + name.replace(" ", "_")
        self.languages = []
        self._fetch_languages()

    def _fetch_languages(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        headings = soup.find_all("h2")
        for heading in headings:
            lang_name = heading.text.strip()
            if lang_name.endswith("[edit]"):
                lang_name = lang_name.replace("[edit]", "")
                lang_codeblocks = []
                next_sibling = heading.next_sibling
                while next_sibling and next_sibling.name != "h2":
                    if next_sibling.name == "pre":
                        codeblock_text = next_sibling.text.strip()
                        codeblock_output = None
                        codeblock_metadata = None
                        # Some code blocks have output or metadata in comments
                        if codeblock_text.startswith("/*"):
                            lines = codeblock_text.split("\n")
                            comment_line = lines[0].strip()
                            if comment_line.endswith("*/"):
                                # Single line comment
                                comment_text = comment_line[2:-2].strip()
                                if comment_text.startswith("Output:"):
                                    codeblock_output = comment_text.replace(
                                        "Output:", ""
                                    ).strip()
                                elif comment_text.startswith("{"):
                                    codeblock_metadata = comment_text
                                codeblock_text = "\n".join(lines[1:]).strip()
                            else:
                                # Multi line comment
                                comment_lines = []
                                i = 0
                                while i < len(lines) and not lines[i].strip().endswith(
                                    "*/"
                                ):
                                    comment_lines.append(lines[i].strip())
                                    i += 1
                                comment_lines.append(lines[i].strip())
                                comment_text = "\n".join(comment_lines)[2:-2].strip()
                                if comment_text.startswith("Output:"):
                                    codeblock_output = comment_text.replace(
                                        "Output:", ""
                                    ).strip()
                                elif comment_text.startswith("{"):
                                    codeblock_metadata = comment_text
                                codeblock_text = "\n".join(lines[i + 1 :]).strip()
                        lang_codeblocks.append(
                            CodeBlock(
                                codeblock_text, codeblock_output, codeblock_metadata
                            )
                        )
                    next_sibling = next_sibling.next_sibling
                print(lang_name, lang_codeblocks)
                self.languages.append(Language(lang_name, lang_codeblocks))

    def to_json(self):
        return {
            "name": self.name,
            "url": self.url,
            "languages": [lang.to_json() for lang in self.languages],
        }


class Language:
    def __init__(self, name, blocks):
        self.name = name
        self.blocks = blocks

    def __repr__(self) -> str:
        return str(len(self.blocks))

    def to_json(self):
        return {"name": self.name, "blocks": [block.to_json() for block in self.blocks]}


class CodeBlock:
    def __init__(self, code, output=None, metadata=None):
        self.code = code
        self.output = output
        self.metadata = metadata

    def to_json(self):
        return {"code": self.code, "output": self.output, "metadata": self.metadata}
