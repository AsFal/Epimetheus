from .TreeLog import TreeLog

import collections
from functools import reduce

from util import flatten

class LogList(collections.MutableSequence):
    def __init__(self, logs=[]):
        self.list = list()
        # self.extend(list(args))
        for log in logs:
            self.append(log)
        super().__init__()

    def check(self, v):
        if not isinstance(v, TreeLog):
            raise TypeError(v)

    def __len__(self): return len(self.list)

    def __getitem__(self, i): return self.list[i]

    def __delitem__(self, i): del self.list[i]

    def __setitem__(self, i, v):
        self.check(v)
        self.list[i] = v

    def insert(self, i, v):
        self.check(v)
        self.list.insert(i, v)

    def getReport(self, category):
        # TODO: getAllCategoryTrees need to be accesssible to this scope
        # Or some general method that returns a common data structure, something like a
        # LogPart (or LogSection)
        # The problem is that I would either have to make merge functions associative between log children
        # I.e. I should be able to TextLog.merge(TreeLog) or vice versa -> this will require some thinking
        # That would require a review of the Merge function
        # For now this will do
        categoryTrees = [log._getAllCategoryTrees() for log in self.list]
        categoryTreesF = [categoryTree for categoryTree in categoryTrees if categoryTree._rootNode.data.isEquivalent(category)]
        reportTree = reduce(lambda merged, categoryTree: merged.merge(categoryTree), categoryTreesF)
        return reportTree.toString()

    def getAllCategories(self):
        return flatten([log.getAllCategories() for log in self.list])

    def getAllCategoryNames(self):
        return flatten([log.getAllcategoryNames() for log in self.list])
