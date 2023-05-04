import argparse
import json
from pathlib import Path
from rosettacode import Category, Task


def main():
    """A command-line interface for scraping code from Rosetta Code."""
    parser = argparse.ArgumentParser(
        description="A command-line interface for scraping code from Rosetta Code."
    )
    parser.add_argument("--task", help="The name of the task to scrape")
    parser.add_argument("--category", help="The name of the category to scrape")
    parser.add_argument("--language", help="The name of the language to filter by")
    parser.add_argument(
        "--list",
        action="store_true",
        help="List the languages and their code blocks for the task or category",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show the code blocks for the task or category",
    )
    parser.add_argument(
        "--json", action="store_true", help="Dump JSON for the task or category data"
    )
    parser.add_argument("--file", help="The name of the file to save the JSON data")
    parser.add_argument(
        "--dir", help="The name of the directory to save the code blocks"
    )
    args = parser.parse_args()

    if args.task:
        item = Task(args.task)
    elif args.category:
        item = Category(args.category)
    else:
        parser.error("You must specify either a task or a category")

    if args.list:
        print(f"Item: {item.name}")
        for lang in item.languages:
            if args.language and args.language not in lang.name:
                continue  # skip this language if it does not match the filter
            print(f"Language: {lang.name}")
            print(f"Code blocks: {len(lang.blocks)}")

    if args.show:
        print(f"Item: {item.name}")
        for lang in item.languages:
            if args.language and args.language not in lang.name:
                continue  # skip this language if it does not match the filter
            print(f"Language: {lang.name}")
            for block in lang.blocks:
                print(f"Code length: {len(block.code)}")
                print(block.code)

    if args.json:
        data = item.to_json()
        if args.file:
            with open(args.file, "w") as f:
                json.dump(data, f)
            print(f"Saved JSON data to {args.file}")
        else:
            print(json.dumps(data, indent=4))

    if args.dir:
        output_dir = Path(args.dir)
        output_dir.mkdir(exist_ok=True)
        for lang in item.languages:
            if args.language and args.language not in lang.name:
                continue  # skip this language if it does not match the filter
            for block in lang.blocks:
                if block.code:
                    file_name = f"{item.name}_{lang.name}.txt"
                    file_path = output_dir / file_name
                    with open(file_path, "w") as f:
                        f.write(block.code)
                    print(f"Saved code to {file_path}")


if __name__ == "__main__":
    main()
