"""
Generates prompts and controls the MadLibs game. Publishes results to an HTML
file and opens it in the user's preferred web browser.
"""

import checklist
from checklist.editor import Editor
import os
import sys
import time
import transformers
from transformers import pipeline
import webbrowser
import numpy as np

GAME_MODE = 0
USER_PROMPT = ""
PROMPT_OUTPUT = ""

def auto():
    print("Give me a sentence-long prompt.")
    print("""For example:
        - Once upon a time, there was a princess and a frog.
        - Today, I want to talk about my dog, Rudy. He is a four-year old English Springer Spaniel.
        - On a dark and stormy evening, I heard a strange rustling from the woods outside my house.""")
    print()
    USER_PROMPT = input("Your prompt: ")
    print()

    generator = pipeline("text-generation", model="distilgpt2")

    PROMPT_OUTPUT = generator(USER_PROMPT,
                            max_length = 1000,
                            num_return_sequences = 1, )

    print()

    PROMPT_OUTPUT = PROMPT_OUTPUT[0].get('generated_text')

    length = len(PROMPT_OUTPUT)
    for char in reversed(range(length)):
        if PROMPT_OUTPUT[char - 1] == '.':
            PROMPT_OUTPUT = PROMPT_OUTPUT[0:char]
            break

    returnResults(PROMPT_OUTPUT)

def default():
    prompt = ""
    return

def returnResults(result):
    timestr = time.strftime("%Y_%m_%d-%H_%M_%S_%p")
    print("Time:", timestr)
    file = 'results_'+timestr+'.html'
    print("Test File Name:", file)

    # to open/create a new html file in the write mode
    resultsFile = open('results_'+timestr+'.html', 'w')

    # the html code which will go in the file results_<date and time>.html
    html_template = """
    <html>
    <head>
        <title>MadLibs ML Results</title>
        <link rel="stylesheet" href="resultStyles.css"/>
    </head>
    <body>
        <h3>MadLibs ML Results</h3>
        <br></br>
        <p>""" + result + """</p>
    </body>
    </html>
    """
    # writing the code into the file
    resultsFile.write(html_template)

    # close the file
    resultsFile.close()

    # 1st method how to open html files in chrome using
    filename = 'file:///'+os.getcwd()+'/' + file
    webbrowser.open_new_tab(filename)

def main():
    print("\nWelcome to MadLibs ML!\n")

    GAME_MODE = int(input("""How would you like to play?
            0 for auto
            1 for default
"""))

    if GAME_MODE == 0:
        print("\nGame Mode: Auto\n")
        auto()
    elif GAME_MODE == 1:
        print("\nGame Mode: Default\n")
    else:
        sys.exit("\nERROR: Invalid game mode\n")

"""

editor = Editor()

ret = editor.template('{first_name} is {a:profession} from {country}.',
                       profession=['lawyer', 'doctor', 'accountant'])
print(np.random.choice(ret.data, 3))
resStr = np.random.choice(ret.data, 3)[0]

"""

if __name__ == '__main__':
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    main()
