from .Log import Log
from treelib import Node, Tree
from .SectionTree import SectionTree
from functools import reduce

from .LogSection import LogSection

# This class should only return Entry objects or strings, NEVER a node
# External classes should never have to interact with the internal behavior of this class

class TreeLogSection(LogSection):
    def __init__(self, tree: SectionTree):
        '''
        Needs a tree for init, cannot be mutated
        '''
        self._log = tree

    def __json__(self, _request):
        return self._log.toString()

    def getAllTitles(self):
        self._log.getAllChildrenTitles(self._log.root)

    def getAllContents(self, level=1):
        self._log.getAllChildrenContent(self._log.root)

    def toString(self):
        return self._log.toString()

