LOG_FILE_PATH = "./logging.txt"
LOG_START = "Log"

from functools import partial
from time import time
from datetime import datetime
from pprint import pprint

from PyInquirer import style_from_dict, Token, prompt

from enum import Enum, auto

# Get file
def getLogs():
    with open(LOG_FILE_PATH) as logs:
        return logs.read()

def isEmpty(string):
    return string == ""

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

def parseBySection(isSectionStart, text: str):
    def findSectionStart(lines, startIndex):
        for index in range(startIndex, len(lines)):
            if isSectionStart(lines[index]):
                return index
        return len(lines)

    def parseSectionsR(sectionsLines, sections):
        sectionIndex = findSectionStart(sectionsLines, 0)
        nextSectionIndex = findSectionStart(sectionsLines, sectionIndex + 1)
        if nextSectionIndex == len(sectionsLines):
            return sections + ["\n".join(sectionsLines[sectionIndex: nextSectionIndex])]
        return parseSectionsR(
            sectionsLines[nextSectionIndex:],
            sections + ["\n".join(sectionsLines[sectionIndex: nextSectionIndex])]
        )

    return parseSectionsR(text.split("\n"), [])


def isLogStart(line):
    return countTabs(line) == 0 and line[0:len(LOG_START)] == LOG_START

parseLogs = partial(parseBySection, isLogStart)

def isLevel(levelNum, line):
    return countTabs(line) == levelNum and not isWhitespace(line)

parseCategories = partial(parseBySection, partial(isLevel, 1))
parseField = partial(parseBySection, partial(isLevel, 2))


class Log(object):
    def __init__(self):
        self._date = self._getDate()
        self._startTime = self._getTime()
        self._level = 1
        self._log = []

    def _getDate(self):
        return ""
    def _getTime(self):
        ts = time()
        return datetime.fromtimestamp(ts).strftime('%H:%M')
    def _tabulation(self):
        return "\t" * self._level

    def levelDown(self):
        self._level -= 1
    def levelUp(self):
        self._level += 1
    def addEntry(self, fieldName, value):
        self._log.append("%s%s: %s" % (self._tabulation(), fieldName, value))
    def getLogString(self):
        return "\n".join(["Log:%s, %s -> %s" % (self._date, self._startTime, self._getTime())] + self._log)

def cli():
    class options(Enum):
        EXIT = auto()
        UP = auto()
        DOWN = auto()
        INPUT = auto()
        SHOW = auto()

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

    def appendLogToFile(log):
        return

    log = Log()

    while True:
        choice = displayOptions()

        if choice == options.EXIT:
            break

        actions = {
            options.DOWN: lambda: log.levelDown(),
            options.UP: lambda: log.levelUp(),
            options.INPUT: newEntry,
            options.SHOW: lambda: print(log.getLogString())
        }
        actions[choice]()

    # appendLogToFile(log.getLogString())

def main():
    logs = getLogs()
    logsArray = parseLogs(logs)
    cli()
    return logsArray

main()