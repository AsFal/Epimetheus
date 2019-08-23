from enum import Enum, auto

from PyInquirer import style_from_dict, Token, prompt

from logs import Log, TextLog, appendToLogs, LogList, TreeLog, Entry

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
    # Add a color option for the suggestions
    # Also tabulate the suggestions to where the input is

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
    title = suggestiveInput(previousTitles, ":")
    sys.stdout.write(" ")
    value = suggestiveInput(previousValues, "\n")
    return Entry(title.strip(), value.strip())

def cli(previousLogs: LogList):

    # Method That seeks in an array of SectionTrees -> SectionLogs, whatever, make an interface
    # Method returns a list of all section titles and contents of level one entries available
    # returns a tuple containing both lists
    # Could also have two methods, one for each, doubles the run time
    # Those arrays can then be passed to the suggestive input so that I can have suggestions of previous
    # categories as I type

    class options(Enum):
        EXIT = auto()
        UP = auto()
        DOWN = auto()
        INPUT = auto()
        SHOW = auto()
        PREVIOUS_CATEGORIES = auto()
        REPORT = auto()

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
                    },
                    {
                        "key": "r",
                        "name": "See a category report",
                        "value": options.REPORT
                    }
                ]
            }
        ]
        answers = prompt(questions)
        return answers[CHOICE]

    def newEntry():
        entry = suggestiveEntry(previousLogs.getAllCategories(), previousLogs.getAllCategoryNames())
        log.addEntry(entry)

    def appendLogToFile(log: Log):
        appendToLogs(log.getLogString())

    def showPreviousCategories():
        pprint(previousLogs.getAllCategories())

    def showReport():
        entry = suggestiveEntry(previousLogs.getAllCategories(), previousLogs.getAllCategoryNames())
        print(previousLogs.getReport(entry))

    log = TreeLog()

    while True:
        choice = displayOptions()

        if choice == options.EXIT:
            break

        actions = {
            options.DOWN: lambda: log.levelDown(),
            options.UP: lambda: log.levelUp(),
            options.INPUT: lambda: newEntry(),
            # TODO
            # Feature imporvement, newEntry takes an array of SectionLogs that share a path from root to it
            # with it, so that the suggestions can be more accurate
            options.SHOW: lambda: print(log.getLogString()),
            options.PREVIOUS_CATEGORIES: showPreviousCategories,
            options.REPORT: lambda: showReport()
        }
        actions[choice]()

    appendLogToFile(log)
