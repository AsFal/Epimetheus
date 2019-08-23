from treelib import Tree, Node
from treelib.exceptions import DuplicatedNodeIdError
from functools import reduce

from .Entry import Entry

from util import find

class SectionTree(Tree):
    def __init__(self, copy=None, tree=None):
        if tree is None:
            super().__init__()
        else:
            super().__init__(tree=tree)

    @property
    def _rootNode(self):
        return self[self.root]

    # This method could be used to absract the knowledge of the Entry to the
    # code using the SectionTree.
    @staticmethod
    def buildEntry(title, content):
        return Entry(title, content)

    def subtree(self, identifier):
        return SectionTree(tree=super().subtree(identifier))

    def addEntry(self, new: Entry, parent=None):
        if parent is None:
            self.create_node(new.title, new.id, data=new)
        else:
            self.create_node(new.title, new.id, parent=parent.id, data=new)

    def toString(self):
        def getLogStringR(tree: SectionTree, level):
            parts = [getLogStringR(tree.subtree(child), level + 1) for child in tree._rootNode.fpointer]
            logString = reduce(lambda previous, new: previous + new, parts, "")
            return "\t" * level + tree._rootNode.data.toString() + "\n" + logString

        return getLogStringR(self, 0)

    def getAllChildSectionTrees(self, nid, condition=None):
        '''
        Condition is on the section subtree
        This Method does not currently have a concept of depth,
        children refers to the root's children.
        '''
        return [
            self.subtree(childNid)
            for childNid in self[nid].fpointer
            if condition is None or condition(self.subtree(nid))]

    def getAllChildrenTitles(self, nid, condition=None):
        return [childTree._rootNode.data.title for childTree in self.getAllChildSectionTrees(nid)]

    def getAllChildrenContent(self, nid, condition=None):
        return [childTree._rootNode.data.content for childTree in self.getAllChildSectionTrees(nid)]

    def _traverse(self, action, builder=None):
        '''
        Again, this methhod does not yet have a concept of depth
        A depth option to specify how deep the traverse method can go would be useful
        '''
        def traverseLogR(self, tree: Tree, action, builder=None):
            if builder is None:
                action(tree)
            else:
                action(tree, builder)
            for nid in tree._rootNode.fpointer:
                traverseLogR(tree.subtree(nid), action, builder)

        traverseLogR(self, action, builder)

    def editEntryTitles(self, old, new):
        def editTitle(tree: Tree):
            if tree._rootNode.data.title == old:
                tree._rootNode.data.title = new
        self._traverse(editTitle)

    def _childNodes(self, node):
        return [self[nid] for nid in node.fpointer]

    # this section should be using the TreeLog data structure instead just the tree data structure
    def merge(self, otherTree):
        def areIdentical(l, r):
            return l.toString() == r.toString()

        def safePaste(targetTree: SectionTree, parentNid, newTree: SectionTree):
            for childNew in newTree._childNodes(newTree._rootNode):
                identicalChildTarget = find(
                    lambda childTarget: areIdentical(childNew.data, childTarget.data),
                    targetTree._childNodes(targetTree._rootNode)
                )
                if identicalChildTarget is None:
                    targetTree.paste(parentNid, newTree.subtree(childNew.identifier))
                else:
                    newSubTree = mergeR(targetTree.subtree(identicalChildTarget.identifier), newTree.subtree(childNew.identifier))
                    targetTree.remove_node(identicalChildTarget.identifier)
                    targetTree.paste(targetTree.root, newSubTree)

        def mergeR(lhs: SectionTree, rhs: SectionTree):
            mergedTree = SectionTree()
            mergedTree.addEntry(lhs._rootNode.data)
            # hopefully this method does not clean the tree

            safePaste(mergedTree, mergedTree.root, lhs)
            safePaste(mergedTree, mergedTree.root, rhs)

            return mergedTree

        return mergeR(self, otherTree)
