LOG_FILE_PATH = "./logging.txt"
LOG_START = "Log"

# from typings import List

from functools import partial, reduce
from time import time
from datetime import datetime
from pprint import pprint

from PyInquirer import style_from_dict, Token, prompt

from enum import Enum, auto
from treelib import Node, Tree

# Get file
def getLogs():
    with open(LOG_FILE_PATH) as logs:
        return logs.read()

def isEmpty(string):
    return string == ""

def flatten(l):
    return [item for sublist in l for item in sublist]

def isWhitespace(string):
    if isEmpty(string):
        return True
    if string[0] != " " or string[0] != "\t":
        return False
    return isWhitespace(string[1:])

def countTabs(line):
    def countTabsR(line, count):
        if isEmpty(line):
            return count
        if line[0] == "\t":
            return countTabsR(line[1:], count + 1)
        return count
    return countTabsR(line, 0)

def findSectionStart(isSectionStart, lines, startIndex):
        for index in range(startIndex, len(lines)):
            if isSectionStart(lines[index]):
                return index
        return len(lines)

def parseBySection(isSectionStart, text: str):
    def parseSectionsR(sectionsLines, sections):
        sectionIndex = findSectionStart(isSectionStart, sectionsLines, 0)
        nextSectionIndex = findSectionStart(isSectionStart, sectionsLines, sectionIndex + 1)
        if nextSectionIndex == len(sectionsLines):
            return sections + ["\n".join(sectionsLines[sectionIndex: nextSectionIndex])]
        return parseSectionsR(
            sectionsLines[nextSectionIndex:],
            sections + ["\n".join(sectionsLines[sectionIndex: nextSectionIndex])]
        )
    return parseSectionsR(text.split("\n"), [])

def extractSectionTitle(isSectionStart, text: str):
    sectionLines = text.split("\n")
    sectionIndex = findSectionStart(isSectionStart, sectionLines, 0)
    return sectionLines[sectionIndex].split(":")[0].strip()

def extractSectionValue(isSectionStart, text: str):
    sectionLines = text.split("\n")
    sectionIndex = findSectionStart(isSectionStart, sectionLines, 0)
    return sectionLines[sectionIndex].split(":")[1].strip()

def isLogStart(line):
    return countTabs(line) == 0 and line[0:len(LOG_START)] == LOG_START

parseLogs = partial(parseBySection, isLogStart)

def isLevel(levelNum, line):
    return countTabs(line) == levelNum and not isWhitespace(line)

parseField = partial(parseBySection, partial(isLevel, 2))

isCategory = partial(isLevel, 1)

class Log(object):
    def __init__(self, oldLog=""):
        self._date = self._getDate()
        self._startTime = self._getTime()
        self._level = 1
        self._log = [] if oldLog == "" else oldLog.split("\n")

    def _getDate(self):
        return datetime.fromtimestamp(time()).strftime("%D")
    def _getTime(self):
        return datetime.fromtimestamp(time()).strftime('%H:%M')
    def _tabulation(self):
        return "\t" * self._level

    # Log interactive creation methods
    def levelDown(self):
        self._level -= 1
    def levelUp(self):
        self._level += 1
    def addEntry(self, fieldName, value):
        self._log.append("%s%s: %s" % (self._tabulation(), fieldName, value))
    def getLogString(self):
        return "\n" + "\n".join(["Log:%s, %s -> %s" % (self._date, self._startTime, self._getTime())] + self._log)

    # Log analysis methods
    def getAllCategories(self):
        parseCategories = partial(parseBySection, isCategory)
        return parseCategories(self.getLogString())
    def getAllCategoryTitles(self):
        categories = self.getAllCategories()
        return [extractSectionTitle(isCategory, category) for category in categories]

    # Log transformation
    # def getCategoryTree():
        # averagedOut ??

class CategoryTree(Tree):
    def __init__(self, category: str):
        super().__init__()
        # use some form of recursive algorithm here to get my tree
    def merge(self, categoryTree):
        return None


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
        with open(LOG_FILE_PATH, "a") as logFile:
            logFile.write(log.getLogString())

    def showPreviousCategories():
        allCategoryTitles = [log.getAllCategoryTitles() for log in previousLogs]
        pprint(sorted(list(set(flatten(allCategoryTitles)))))

    log = Log()

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
