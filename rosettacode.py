import logging
import requests
from bs4 import BeautifulSoup


class Category:
    """A class that represents a category page on Rosetta Code."""

    def __init__(self, name):
        """Initialize the category with a name and a list of tasks."""
        self.name = name
        self.tasks = []
        self._fetch_tasks()

    def _fetch_tasks(self):
        """Fetch the tasks from the category page using requests and BeautifulSoup."""
        url = f"https://rosettacode.org/wiki/Category:{self.name}"
        logging.info(f"Fetching tasks from {url}")
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            task_list = soup.find("div", id="mw-pages")
            if task_list:
                task_links = task_list.find_all("a")
                for link in task_links:
                    task_name = link.text
                    self.tasks.append(Task(task_name))
            else:
                logging.warning(f"No tasks found for category {self.name}")
        else:
            logging.error(f"Failed to fetch tasks from {url}: {response.status_code}")

    def to_json(self):
        """Return a JSON-serializable representation of the category."""
        return {"name": self.name, "tasks": [task.to_json() for task in self.tasks]}


class Task:
    """A class that represents a task page on Rosetta Code."""

    def __init__(self, name):
        """Initialize the task with a name and a list of languages."""
        self.name = name
        self.languages = []
        self._fetch_languages()

    def _fetch_languages(self):
        """Fetch the languages from the task page using requests and BeautifulSoup."""
        url = f"https://rosettacode.org/wiki/{self.name}"
        logging.info(f"Fetching languages from {url}")
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            language_list = soup.find("div", id="toc")
            if language_list:
                language_links = language_list.find_all("a")[
                    1:
                ]  # skip the first link which is not a language
                for link in language_links:
                    language_name = link.text
                    self.languages.append(Language(language_name, self.name))
            else:
                logging.warning(f"No languages found for task {self.name}")
        else:
            logging.error(
                f"Failed to fetch languages from {url}: {response.status_code}"
            )

    def to_json(self):
        """Return a JSON-serializable representation of the task."""
        return {
            "name": self.name,
            "languages": [lang.to_json() for lang in self.languages],
        }


class Language:
    """A class that represents a language section on a task page on Rosetta Code."""

    def __init__(self, name, task_name):
        """Initialize the language with a name, a task name, and a list of code blocks."""
        self.name = name
        self.task_name = task_name
        self.blocks = []
        self._fetch_blocks()

    def _fetch_blocks(self):
        """Fetch the code blocks from the language section using requests and BeautifulSoup."""
        url = f"https://rosettacode.org/wiki/{self.task_name}#{self.name}"
        logging.info(f"Fetching code blocks from {url}")
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            language_section = soup.find("span", id=self.name).parent
            if language_section:
                code_tags = language_section.find_all("pre")
                for tag in code_tags:
                    block = CodeBlock(tag)
                    self.blocks.append(block)
            else:
                logging.warning(
                    f"No code blocks found for language {self.name} in task {self.task_name}"
                )
        else:
            logging.error(
                f"Failed to fetch code blocks from {url}: {response.status_code}"
            )

    def to_json(self):
        """Return a JSON-serializable representation of the language."""
        return {"name": self.name, "blocks": [block.to_json() for block in self.blocks]}


class CodeBlock:
    """A class that represents a code block on a language section on Rosetta Code."""

    def __init__(self, tag):
        """Initialize the code block with a BeautifulSoup tag and extract its attributes."""
        self.tag = tag
        self.code = tag.text
        self.output = None
        self.metadata = {}
        self._extract_attributes()

    def _extract_attributes(self):
        """Extract the attributes of the code block from its tag."""
        # check if the tag has a class attribute
        if self.tag.has_attr("class"):
            # get the value of the class attribute as a list
            classes = self.tag["class"]
            # loop through the classes
            for cls in classes:
                # check if the class starts with "output-"
                if cls.startswith("output-"):
                    # get the output type after the dash
                    output_type = cls.split("-")[1]
                    # set the output attribute to the output type
                    self.output = output_type
                # check if the class is "works-with"
                elif cls == "works-with":
                    # get the next sibling tag, which should be a span tag
                    span_tag = self.tag.next_sibling
                    # check if the span tag has a title attribute
                    if span_tag and span_tag.has_attr("title"):
                        # get the value of the title attribute as a string
                        works_with = span_tag["title"]
                        # set the metadata attribute with the key "works-with" and the value as a list of works-with items
                        self.metadata["works-with"] = works_with.split(", ")
                # check if the class is "lang"
                elif cls == "lang":
                    # get the next sibling tag, which should be a span tag
                    span_tag = self.tag.next_sibling
                    # check if the span tag has a text attribute
                    if span_tag and span_tag.text:
                        # get the value of the text attribute as a string
                        lang = span_tag.text
                        # set the metadata attribute with the key "lang" and the value as a list of lang items
                        self.metadata["lang"] = lang.split(", ")
