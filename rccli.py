import requests
from bs4 import BeautifulSoup
import argparse
import os
from progress_bar import progress_bar

parser = argparse.ArgumentParser()
parser.add_argument("--task", help="Scrape a specific task by name")
parser.add_argument("--output", default="/Users/ash/Desktop/rosettacode/code", help="Output directory for scraped tasks")
args = parser.parse_args()

output_dir = args.output
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def scrape_task(task_name):
    url = f"https://rosettacode.org/wiki/{task_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    pre_tags = soup.find_all("pre")

    supported_languages = {
        "c": ".c",
        "c++": ".cpp",
        "rust": ".rs",
        "haskell": ".hs",
        "java": ".java"
    }

    for pre_tag in pre_tags:
        div_tag = pre_tag.find_previous("div")
        if div_tag is not None and div_tag.find("dl"):
            dt_tag = div_tag.find("dt")
            if dt_tag is not None and dt_tag.text.strip() == "Output:":
                continue

        h2_tag = pre_tag.find_previous("h2")
        if h2_tag is None:
            continue

        lang = h2_tag.text.strip()
        lang = lang.replace("[edit]", "")
        lang = lang.replace("\\", "\\\\")
        lang = lang.replace("/", "-")
        code = pre_tag.text.strip()

        if lang.lower() not in supported_languages:
            continue

        lang_dir = os.path.join(output_dir, lang)
        os.makedirs(lang_dir, exist_ok=True)

        file_extension = supported_languages[lang.lower()]
        file_name = f"{task_name}{file_extension}"
        file_path = os.path.join(lang_dir, file_name)

        try:
            # Create parent directories recursively if they don't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, "wb") as f:
                f.write(code.encode("utf-8"))
        except OSError as e:
            print(f"Failed to write file: {file_path}. Error: {str(e)}")


def scrape_rosetta_code():
    base_url = "https://rosettacode.org"
    tasks_url = base_url + "/wiki/Category:Programming_Tasks"

    response = requests.get(tasks_url)
    soup = BeautifulSoup(response.text, "html.parser")
    page_links = soup.find_all("a", class_="mw-category-page-link")

    for page_link in page_links:
        page_url = base_url + page_link["href"]
        page_response = requests.get(page_url)
        page_soup = BeautifulSoup(page_response.text, "html.parser")
        task_links = page_soup.find_all("a", class_="mw-category")

        for task_link in task_links:
            task_name = task_link.text.strip()
            scrape_task(task_name)


# Scrape a specific task if provided
if args.task:
    task_name = args.task
    scrape_task(task_name)
    print(f"Scraped task: {task_name}")
else:
    # Scrape all tasks
    print("Scraping tasks from Rosetta Code...")

    # Get the list of all tasks
    url = "https://rosettacode.org/wiki/Category:Programming_Tasks"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    task_links = soup.select("#mw-pages .mw-category-group ul li a")

    total_tasks = len(task_links)
    current_task = 0

    progress_bar(0, total_tasks)
    for task_link in task_links:
        task_name = task_link.text.strip()
        scrape_task(task_name)
        current_task += 1
        progress_bar(current_task, total_tasks)

    print("Scraping completed.")
