import argparse
import json
import os
from rosettacode import Category, Task

parser = argparse.ArgumentParser(description="A CLI-tool for scraping source code")
parser.add_argument("--task", help="The name of the task to scrape")
parser.add_argument("--category", help="The name of the category to scrape")
parser.add_argument("--languages", action="store_true", help="List the languages in the task or category")
parser.add_argument("--count", action="store_true", help="Show the number of code blocks for each language")
parser.add_argument("--language", help="The name of the language to filter by")
parser.add_argument("--code", action="store_true", help="Show the code blocks for the task or category")
parser.add_argument("--json", action="store_true", help="Dump JSON for the task or category data")
parser.add_argument("--file", help="The name of the file to save the JSON data")
parser.add_argument("--dir", help="The name of the directory to save the code blocks")

args = parser.parse_args()

if args.task:
    # Scrape a task
    task = Task(args.task)
    if args.languages:
        # List the languages in the task
        for lang in task.languages:
            if args.count:
                # Show the number of code blocks for each language
                print("{}: {}".format(lang.name, len(lang.blocks)))
            else:
                print(lang.name)
    elif args.code:
        # Show the code blocks for the task
        if args.language:
            # Filter by a specific language
            lang = next((lang for lang in task.languages if lang.name == args.language), None)
            if lang:
                for block in lang.blocks:
                    print(block.code)
                    print()
            else:
                print("Language not found: {}".format(args.language))
        else:
            # Show all the code blocks for all languages
            for lang in task.languages:
                print(lang.name)
                print()
                for block in lang.blocks:
                    print(block.code)
                    print()
    elif args.json:
        # Dump JSON for the task data
        data = task.to_json()
        if args.file:
            # Save the JSON data to a file
            with open(args.file, "w") as f:
                json.dump(data, f, indent=4)
        else:
            # Print the JSON data to stdout
            print(json.dumps(data, indent=4))
    elif args.dir:
        # Save the code blocks to a directory
        if not os.path.exists(args.dir):
            os.makedirs(args.dir)
        if args.language:
            # Filter by a specific language
            lang = next((lang for lang in task.languages if lang.name == args.language), None)
            if lang:
                for i, block in enumerate(lang.blocks):
                    filename = "{}_{}_{}.txt".format(task.name, lang.name, i+1)
                    filepath = os.path.join(args.dir, filename)
                    with open(filepath, "w") as f:
                        f.write(block.code)
            else:
                print("Language not found: {}".format(args.language))
        else:
            # Save all the code blocks for all languages
            for lang in task.languages:
                for i, block in enumerate(lang.blocks):
                    filename = "{}_{}_{}.txt".format(task.name, lang.name, i+1)
                    filepath = os.path.join(args.dir, filename)
                    with open(filepath, "w") as f:
                        f.write(block.code)

elif args.category:
    # Scrape a category
    category = Category(args.category)
    if args.tasks:
        # List the tasks in the category
        for task in category.tasks:
            print(task.name)
    elif args.code:
        # Show the code blocks for the category
        if args.language:
            # Filter by a specific language
            for task in category.tasks:
                lang = next((lang for lang in task.languages if lang.name == args.language), None)
                if lang:
                    print(task.name)
                    print()
                    for block in lang.blocks:
                        print(block.code)
                        print()
        else:
            # Show all the code blocks for all languages
            for task in category.tasks:
                print(task.name)
                print()
                for lang in task.languages:
                    print(lang.name)
                    print()
                    for block in lang.blocks:
                        print(block.code)
                        print()
    elif args.json:
        # Dump JSON for the category data
        data = category.to_json()
        if args.file:
            # Save the JSON data to a file
            with open(args.file, "w") as f:
                json.dump(data, f, indent=4)
        else:
            # Print the JSON data to stdout
            print(json.dumps(data, indent=4))
    elif args.dir:
        # Save the code blocks to a directory
        if not os.path.exists(args.dir):
            os.makedirs(args.dir)
        if args.language:
            # Filter by a specific language
            for task in category.tasks:
                lang = next((lang for lang in task.languages if lang.name == args.language), None)
                if lang:
                    for i, block in enumerate(lang.blocks):
                        filename = "{}_{}_{}.txt".format(task.name, lang.name, i+1)
                        filepath = os.path.join(args.dir, filename)
                        with open(filepath, "w") as f:
                            f.write(block.code)
        else: 
            # Save all the code blocks for all languages
            for task in category.tasks: 
                for lang in task.languages: 
                    for i, block in enumerate(lang.blocks): 
                        filename = "{}_{}_{}.txt".format(task.name, lang.name, i+1) 
                        filepath = os.path.join(args.dir, filename) 
                        with open(filepath, "w") as f: 
                            f.write(block.code)

else: 
    # No arguments given 
    parser.print_help()
