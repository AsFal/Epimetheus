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

parseLogs = partial(parseBySection, isLogStart)

def main():
    logs = getLogs()
    logsArray = parseLogs(logs)
    return logsArray

main()



# Analyse by tabs, counttab function
# Make tree from it
# Save tree somewhere else as well
#
# Save in the safe website by scraping the web a little, with da python
#
# Log writer CLI interface
#