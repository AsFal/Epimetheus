from datetime import datetime
from time import time

from functools import partial

from .textParser import parseBySection, isCategory, extractSectionTitle

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

