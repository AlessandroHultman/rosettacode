# Program for reading source code from Rosetta Code Data Project

## Introduction
The rosettacode.org site provides example code for a variety for different tasks in many different languages. Because the code is generally pretty self contained and simple - as the point is to show the differences in the way languages do things - it makes a good source of code to try things out with. I used this to test an LLVM analysis pass for example.

The `rccli.py` script can be used to read source code and nothing more from the Task page.

## Getting started
### Dependencies
- beautifulsoup4
- requests
- colorama
### Using pipenv
- `$ pip install pipenv`
- `$ cd rosettacode`
- `$ pipenv install`
- `$ pipenv shell`
## Running the program
Example use:
```
$ python rccli.py
```
The program will scrape the source code for all tasks for all languages specified in the supported_languages dictionary declared on line 22.
