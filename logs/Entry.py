from datetime import datetime
from time import time

from random import random

class Entry(object):
    @staticmethod
    def fromString(stringEntry):
        '''
        Supports parsing entry of the following format:\n
        Entry Title: Entry Content
        '''
        entryParts = stringEntry.split(":")
        return Entry(entryParts[0].strip(), ":".join(entryParts[1:]).strip())

    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.id = self._setId()

    def _setId(self):
        return str(int(random() * 10000000)) # TODO, change this for something more reliable

    def toString(self):
        return "%s: %s" % (self.title, self.content)

    def isEquivalent(self, entry):
        '''
        Returns true when title and content of both entries are the same.
        '''
        return self.title == entry.title and self.content == entry.content

class LogHeader(Entry):

    @staticmethod
    def fromString(stringEntry):
        """
        :param stringEntry: existing string entry
        :type stringEntry: str
        :rtype: LogHeader
        """
        entry = Entry.fromString(stringEntry)
        dateTime = entry.content.split(",")
        startFinish = dateTime[1].split("->")
        return LogHeader(dateTime[0].strip(), startFinish[0].strip(), startFinish[1].strip())

    def __init__(self, date=None, startTime=None, endTime=None):
        self.date = self._getDate() if date is None else date
        self.startTime = self._getTime() if startTime is None else startTime
        self.endTime = endTime
        super().__init__(self.title, self.content)

    def _getDate(self):
        return datetime.fromtimestamp(time()).strftime("%D")
    def _getTime(self):
        return datetime.fromtimestamp(time()).strftime('%H:%M')

    @property
    def content(self):
        return "%s, %s -> %s" % (
            self.date,
            self.startTime,
            self._getTime() if self.endTime == None else self.endTime
        )

    @content.setter
    def content(self, _):
        pass

    @property
    def title(self):
        return "Log"

    @title.setter
    def title(self, _):
        pass

