LOG_FILE_PATH = "./logging.txt"
LOG_START = "Log"

from functools import partial

# Get file
def getLogs():
    with open(LOG_FILE_PATH) as logs:
        return logs.read()

def isEmpty(string):
    return string == ""

def countTabs(line):
    def countTabsR(line, count):
        if isEmpty(line):
            return count
        if line[0] == "\t":
            return countTabsR(line[1:], count + 1)
        return count
    return countTabsR(line, 0)

def isLogStart(line):
    return countTabs(line) == 0 and line[0:len(LOG_START)] == LOG_START

def parseLogs(logs: str):  # returns array of log strings
    def findLogStartIndex(logsLines, startIndex):
        for index in range(startIndex, len(logsLines)):
            if isLogStart(logsLines[index]):
                return index
        return len(logsLines)

    def parseLogsR(logsLines, logsArray):
        logIndex = findLogStartIndex(logsLines, 0)
        nextLogIndex = findLogStartIndex(logsLines[logIndex:], logIndex + 1)
        if nextLogIndex == len(logsLines):
            return logsArray + ["\n".join(logsLines[logIndex: nextLogIndex])]
        return parseLogsR(logsLines[nextLogIndex:], logsArray + ["\n".join(logsLines[logIndex: nextLogIndex])])

    return parseLogsR(logs.split("\n"), [])

def main():
    logs = getLogs()
    logsArray = parseLogs(logs)
    return logsArray

main()


# def parseBySection(isSectionStart, text: str):
#     def findSectionStart(isSectionStart, text, startIndex):
#         for line in range(index, len(logsLines)):
#             if isSectionStart(line):
#                 return index
#         return len(logsLines)
#
#     def parseSectionsR(sectionsLines, sections):
#         sectionIndex = findSectionStart(sectionsLines, 0)
#         nextSectionIndex = findSectionStart(sectionsLines, sectionIndex + 1)
#         if nextSectionIndex == len(sectionsLines):
#             return sections + ["\n".join(sectionsLines[sectionIndex: nextSectionIndex])]
#         return parseLogsR(
#             sectionsLines[nextSectionIndex:],
#             sections + ["\n".join(sections[sectionIndex: nextSectionIndex])]
#         )
#
#     return parseSectionsR(logs.split("\n"), [])


# Analyse by tabs, counttab function
# Make tree from it
# Save tree somewhere else as well
#
# Save in the safe website by scraping the web a little, with da python
#
# Log writer CLI interface
#