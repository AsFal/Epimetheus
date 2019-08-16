from enum import Enum, auto

from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt

from logs import Log, TextLog, appendToLogs

from util import flatten
from getch import getch
from pprint import pprint



def startWith(word, prefix):
    return word.lower()[0: len(prefix)] == prefix.lower()

def autocompleteGenerator(availableWords):
    def getSuggestions(partialWord):
        return [word for word in availableWords if startWith(word, partialWord)]
    return getSuggestions


def suggestiveInput(availableWords):
    ENTER_ORDER = 10
    BACKSPACE_ORDER = 127
    '''As input is written, the user will be able to see suggestions in the terminal'''
    suggestions = autocompleteGenerator(availableWords)
    # Before : suggest different different categories
    word = ""
    while True:
        c = getch()
        if ord(c) == ENTER_ORDER:
            break
        elif ord(c) == BACKSPACE_ORDER:
            word = word[0:-1]
        else:
            word += c
        print("==================")
        print(word)
        pprint(suggestions(word))
        print("------------------")
    return word


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
