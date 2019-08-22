from .TreeLog import TreeLog

from functools import reduce

from util import flatten

class LogList(list):
    def __init__(self, logs=[]):
        for log in logs:
            self.append(log)
        super.__init__()

    def append(self, new):
        assert isinstance(new, TreeLog)
        super().append(new)

    def getReport(self, category):
        # TODO: getAllCategoryTrees need to be accesssible to this scope
        # Or some general method that returns a common data structure, something like a
        # LogPart (or LogSection)
        # The problem is that I would either have to make merge functions associative between log children
        # I.e. I should be able to TextLog.merge(TreeLog) or vice versa -> this will require some thinking
        # That would require a review of the Merge function
        # For now this will do
        categoryTrees = [log._getAllCategoryTrees() for log in self]
        categoryTreesF = [categoryTree for categoryTree in categoryTrees if categoryTree._rootNode.data.isEquivalent(category)]
        reportTree = reduce(lambda merged, categoryTree: merged.merge(categoryTree), categoryTreesF)
        return reportTree.toString()

    def getAllCategoryTitles(self):
        return flatten([log.getAllCategories() for log in self])

    def getAllCategoryNames(self):
        return flatten([log.getAllcategoryNames() for log in self])

