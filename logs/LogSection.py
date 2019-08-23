# For now, this will stay a readonly interface
class LogSection(object):
    def getAllTitles(self, level=1):
        raise NotImplementedError

    def getAllContents(self, level=1):
        raise NotImplementedError

    def subSection(self):
        raise NotImplementedError
