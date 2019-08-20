from datetime import datetime
from time import time

from .SectionTree import Entry

from functools import partial

from .textParser import parseBySection, isCategory, extractSectionTitle
class Log(object):
    _level = 1
    def __init__(self, header = None):
        if header is None:
            self._date = self._getDate()
            self._startTime = self._getTime()
            self._endTime = None
        else:
            self._date = header[0]
            self._startTime = header[1]
            self._endTime = header[2]


    def _getDate(self):
        return datetime.fromtimestamp(time()).strftime("%D")
    def _getTime(self):
        return datetime.fromtimestamp(time()).strftime('%H:%M')

    def _buildLogHeader(self):
        return Entry(
            "Log",
            "%s, %s -> %s" % (
                self._date,
                self._startTime,
                self._getTime() if self._endTime == None else self._endTime
            )
        )

    def _parseLogHeaderString(self, header):
        entry = Entry.fromString(header)

        dateTime = entry.content.split(",")
        startFinish = dateTime[1].split("->")
        return (dateTime[0].strip(), startFinish[0].strip(), startFinish[1].strip())

    def setDate(self, date):
        # check format of date or something
        self._date = date
    def setStartTime(self, time):
        self._startTime = time
    def setEndTime(self, time):
        self._endTime = time

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

