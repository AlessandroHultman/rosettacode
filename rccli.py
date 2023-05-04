from progress_bar import progress_bar

import requests
from bs4 import BeautifulSoup
import argparse
import os

# Define the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--task', help='The name of the task to scrape')
args = parser.parse_args()

# Check if the task argument is given
if args.task:
    # Construct the URL of the task page
    url = f'https://rosettacode.org/wiki/{args.task}'
    # Make a request to the URL and get the HTML content
    response = requests.get(url)
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all the <pre> tags that contain the source code
    pre_tags = soup.find_all('pre')
    index = 0;
    progress_bar(index, len(pre_tags))
    # Loop through each <pre> tag
    for pre_tag in pre_tags:
        # Get the name of the programming language from the previous <h2> tag
        lang = pre_tag.find_previous('h2').text.strip()
        # Remove the "[edit]" part from the language name
        lang = lang.replace('[edit]', '')
        # Escape the backslashes in the language name
        lang = lang.replace('\\', '\\\\')
        # Replace the slashes in the language name with dashes
        lang = lang.replace('/', '-')
        # Get the source code from the <pre> tag
        code = pre_tag.text.strip()
        # Create a directory named 'code' if it does not exist
        if not os.path.exists(args.task):
            os.mkdir(args.task)
        # Create a file named '<language>.txt' in the 'code' directory
        file_name = f'{lang}.txt'
        file_path = os.path.join(args.task, file_name)
        # Write the source code to the file
        with open(file_path, 'w') as f:
            f.write(code)
        index = index + 1
        progress_bar(index, len(pre_tags))
else:
    # Print a message indicating the task argument is missing
    print('Please provide a task name using --task argument')
