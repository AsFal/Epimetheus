from .Log import Log
from treelib import Node, Tree
from .SectionTree import SectionTree

from functools import reduce

# This class should only return Entry objects or strings, NEVER a node
# External classes should never have to interact with the internal behavior of this class

class TreeLog(Log):

    @staticmethod
    def getReport(self, logs, category): # -> all logs must be TreeLog
        categoryTrees = [log._getAllCategoryTrees() for log in logs]
        categoryTreesF = [categoryTree for categoryTree in categoryTrees if categoryTree._rootNode.data.id == category.id]
        reportTree = reduce(lambda merged, categoryTree: merged.merge(categoryTree), categoryTreesF)
        return reportTree.toString()

    def __init__(self):
        super().__init__()
        self._log = SectionTree()
        self._log.addEntry(self.header)
        self._iteratorParent = self.header
        self._lastEntry = None

    def getLogHeader(self):
        return self._log[self._log.root].data

    def levelUp(self):
        self._iteratorParent = self._lastEntry
        self._lastEntry = None

    def levelDown(self):
        self._iteratorParent = self._log[self._log[self._iteratorParent.id].bpointer].data
        self._lastEntry = self._iteratorParent

    def addEntry(self, new, parent=None):
        '''
        Provide parent entry in the form of a tuple
        (title, content)
        '''
        parent = self._iteratorParent if parent is None else parent
        self._lastEntry = new
        self._log.addEntry(new, parent)
        # build iterator that can follow where to go based on level up level down

    def getLogString(self):
        return self._log.toString()

    def getAllCategorySections(self):
        return [subTree.toString() for subTree in self._getAllCategoryTrees()]

    def _getAllCategoryTrees(self, condition=None):
        return self._log.getAllChildSectionTrees()

    def getAllCategories(self):
        return self._log.getAllChildrenTitles(self._log._rootNode)

    def getAllCategoryNames(self):
        return self._log.getAllChildrenContent(self._log._rootNode)

    def editEntryTitles(self, old, new):
        self._log.editEntryTitles(old, new)
