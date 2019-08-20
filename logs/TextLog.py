from .Log import Log
from datetime import datetime
from time import time

from .TreeLog import TreeLog
from .SectionTree import Entry

from functools import partial

from .textParser import parseBySection, isCategory, extractSectionTitle, isCategory, isLevel, isLogStart, findSectionStart

class TextLog(Log):


    # Three tree does not support duplicate nodes, although this logging structure currently supports it
    # Either they both must support it, or none do, for now, this shall be documented in the test and not mentioned
    # CRITICAL BUG
    # Answer, I have to find a way to support it!!
    def toTreeLog(self):
        def toTreeLogR(sectionLines, level, parent, tree: TreeLog):
            # find first line and extract title
            isSectionStart = partial(isLevel, level)
            if len(sectionLines) == 0\
            or len(sectionLines) ==findSectionStart(isSectionStart, sectionLines):
                return
            nextIndex = 0
            while nextIndex != len(sectionLines):
                # find entry
                sectionIndex = findSectionStart(isSectionStart, sectionLines, nextIndex)
                nextIndex = findSectionStart(isSectionStart, sectionLines, sectionIndex + 1)

                # add entry to tree
                newEntry = Entry.fromString(sectionLines[sectionIndex])
                treeLog.addEntry(newEntry, parent)
                toTreeLogR(sectionLines[sectionIndex + 1: nextIndex], level + 1, newEntry, tree)

        treeLog = TreeLog()
        treeLog.setDate(self._date)
        treeLog.setStartTime(self._startTime)
        treeLog.setEndTime(self._endTime)
        toTreeLogR(self._log, 1, treeLog.getLogHeader(), treeLog)
        return treeLog

    # This could eventually be extracted in another data structure similar to the SectionTree one
    # A general parser data structure
    def _findSectionStart(self, isSectionStart, lines, startIndex=0):
        '''
            Searches a list of lines for the start of a section,
            as defined by the isSectionStart function, and returns
            the index of the start line. If no line is found, the
            length of the lines list is returned.
        '''
        for index in range(startIndex, len(lines)):
            if isSectionStart(lines[index]):
                return index
        return len(lines)

    def __init__(self, oldLog=""):
        # Need a remove whitespace empty whitespace lines
        if oldLog == "":
            super().__init__()
            self._log = []
        else:
            oldLogLines = oldLog.split("\n")
            logHeaderIndex = findSectionStart(isLogStart, oldLogLines)
            self._log = oldLogLines[logHeaderIndex + 1:]
            oldHeader = self._parseLogHeaderString(oldLogLines[logHeaderIndex])
            super().__init__(oldHeader)

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
        return "\n".join([self._buildLogHeader().toString()] + self._log)

    # Log analysis methods
    def getAllCategories(self):
        parseCategories = partial(parseBySection, isCategory)
        return parseCategories(self.getLogString())
    def getAllCategoryTitles(self):
        categories = self.getAllCategories()
        return [extractSectionTitle(isCategory, category) for category in categories]