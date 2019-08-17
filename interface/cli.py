from enum import Enum, auto

from PyInquirer import style_from_dict, Token, prompt

from logs import Log, TextLog, appendToLogs

from util import flatten
from getch import getch
from pprint import pprint

import sys

def startWith(word, prefix):
    return word.lower()[0: len(prefix)] == prefix.lower()

def autocompleteGenerator(availableWords):
    def getSuggestions(partialWord):
        return [word for word in availableWords if startWith(word, partialWord)]
    return getSuggestions

def suggestiveInput(availableWords, endCharacter):

    CLEAR_REST = "\033[K"
    BACKSPACE_ORDER = 127

    def saveCursor():
        sys.stdout.write("\033[s") # ANSI escpae sequences
    def returntoSave():
        sys.stdout.write("\033[u")

    '''As input is written, the user will be able to see suggestions in the terminal'''
    suggestions = autocompleteGenerator(availableWords)
    # Before : suggest different different categories
    word = ""
    while True:
        c = getch()
        if ord(c) == ord(endCharacter):
            sys.stdout.write(word + endCharacter)
            sys.stdout.flush()
            break
        elif ord(c) == BACKSPACE_ORDER:
            word = word[0:-1]
        else:
            word += c

        saveCursor()
        sys.stdout.write("%s%s\n" % (word, CLEAR_REST)) # write word inline and clear rest of line
        options = suggestions(word)
        for i in range(0, 5):
            if i < len(options):
                print(options[i] + CLEAR_REST)
            else:
                print(CLEAR_REST)
        returntoSave()

    return word

def suggestiveEntry(previousTitles, previousValues):
    ENTER_ORDER = 10
    title = suggestiveInput(previousTitles, ":")
    sys.stdout.write(" ")
    value = suggestiveInput(previousValues, "\n")
    return (title.strip(), value.strip())

def cli(previousLogs):
    class options(Enum):
        EXIT = auto()
        UP = auto()
        DOWN = auto()
        INPUT = auto()
        SHOW = auto()
        PREVIOUS_CATEGORIES = auto()

    def displayOptions():
        CHOICE = "choice"
        questions = [
            {
                "type": "expand",
                "name": CHOICE,
                "message": "Log options",
                "choices": [
                    {
                        "key": "d",
                        "name": "Go Down a level",
                        "value": options.DOWN
                    },
                    {
                        "key": "u",
                        "name": "Go up a level",
                        "value": options.UP
                    },
                    {
                        "key": "e",
                        "name": "Entry",
                        "value": options.INPUT
                    },
                    {
                        "key": "s",
                        "name": "Show Log",
                        "value": options.SHOW
                    },
                    {
                        "key": "x",
                        "name": "Save and exit",
                        "value": options.EXIT
                    },
                    {
                        "key": "p",
                        "name": "Previous chosen categories",
                        "value": options.PREVIOUS_CATEGORIES
                    }
                ]
            }
        ]
        answers = prompt(questions)
        return answers[CHOICE]

    def newEntry():
        entry = input()
        entryParts = [part.strip() for part in entry.split(":")]
        log.addEntry(entryParts[0], entryParts[1])

    def appendLogToFile(log: Log):
        appendToLogs(log.getLogString())

    def showPreviousCategories():
        allCategoryTitles = [log.getAllCategoryTitles() for log in previousLogs]
        pprint(sorted(list(set(flatten(allCategoryTitles)))))

    log = TextLog()

    while True:
        choice = displayOptions()

        if choice == options.EXIT:
            break

        actions = {
            options.DOWN: lambda: log.levelDown(),
            options.UP: lambda: log.levelUp(),
            options.INPUT: newEntry,
            options.SHOW: lambda: print(log.getLogString()),
            options.PREVIOUS_CATEGORIES: showPreviousCategories
        }
        actions[choice]()

    appendLogToFile(log)
