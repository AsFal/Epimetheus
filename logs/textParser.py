LOG_FILE_PATH = "./entities/logging.txt"
LOG_START = "Log"

from functools import partial, reduce
from enum import Enum, auto

from util import countTabs, isWhitespace

# Get file
def getLogs():
    with open(LOG_FILE_PATH) as logs:
        return logs.read()

def appendToLogs(newLogString):
    with open(LOG_FILE_PATH, "a") as logFile:
        logFile.write(newLogString)

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

