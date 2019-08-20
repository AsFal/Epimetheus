from datetime import datetime
from time import time

from .Entry import Entry, LogHeader

from .SectionTree import Entry

from functools import partial

from .textParser import parseBySection, isCategory, extractSectionTitle
class Log(object):
    _level = 1
    def __init__(self, date=None, startTime=None, endTime=None):
        self.header = LogHeader(date, startTime, endTime)

    @property
    def _date(self):
        return self.header.date
    @property
    def _startTime(self):
        return self.header.startTime
    @property
    def _endTime(self):
        return self.header.endTime

    @_date.setter
    def _date(self, date):
        self.header.date = date
    @_startTime.setter
    def _startTime(self, time):
        self.header.startTime = time
    @_endTime.setter
    def _endTime(self, time):
        self.header.endTime = time


    # Log interactive creation methods
    def levelDown(self):
        self._level -= 1
    def levelUp(self):
        self._level += 1

    def addEntry(self, fieldName, value):
        raise NotImplementedError
    def getLogString(self):
        raise NotImplementedError

    def getAllCategories(self):
        raise NotImplementedError
    def getAllCategoryTitles(self):
        raise NotImplementedError