from treelib import Tree, Node
from treelib.exceptions import DuplicatedNodeIdError
from functools import reduce

from util import find

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

    @property
    def id(self):
        return self.title + self.content

    def toString(self):
        return "%s: %s" % (self.title, self.content)

# TopLevel Class must have an iterator

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

    def getLogString(self):
        return self.toString()

    def toString(self):
        def getLogStringR(tree: SectionTree, level):
            parts = [getLogStringR(tree.subtree(child), level + 1) for child in tree._rootNode.fpointer]
            logString = reduce(lambda previous, new: previous + new, parts, "")
            return "\t" * level + tree._rootNode.data.toString() + "\n" + logString

        return getLogStringR(self, 0)

    def getAllChildSectionTrees(self, condition=None):
        '''
        Condition is on the section subtree
        This Method does not currently have a concept of depth,
        children refers to the root's children.
        '''
        return [
            self.subtree(node.tag)
            for node in self._rootNode.fpointer
            if condition is None or condition(self.subtree(node.tag))]

    def getAllChildrenTitles(self, root, condition=None):
        return [childTree._rootNode.data.title for childTree in self.getAllChildSectionTrees()]

    def getAllChildrenContent(self, root, condition=None):
        return [childTree._rootNode.data.content for childTree in self.getAllChildSectionTrees()]

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
            for child in tree._rootNode.fpointer:
                traverseLogR(tree.subtree(child.tag), builder, builder)

        traverseLogR(self, action, builder)

    def editEntryTitles(self, old, new):
        def editTitle(tree: Tree):
            if tree._rootNode.data.title == old:
                tree._rootNode.data.title = new
        self._traverse(editTitle)

    # this section should be using the TreeLog data structure instead just the tree data structure
    def merge(self, otherTree):

        # def clean(tree: SectionTree):
        #     cleanTree = SectionTree()
        #     cleanTree.add_node(tree._rootNode)
        #     for childNid in tree._rootNode.fpointer:
        #         if any(nid == childNid for nid in cleanTree._rootNode.fpointer):
        #             newTree = mergeR(cleanTree.subtree(childNid), tree.subtree(childNid))
        #             cleanTree.remove_node(childNid)
        #             cleanTree.add_node(newTree._rootNode)
        #     return cleanTree

        def safePaste(targetTree: SectionTree, parent, newTree: SectionTree):
            for nid in newTree._rootNode.fpointer:
                if nid not in targetTree._rootNode.fpointer:
                    targetTree.paste(targetTree.root, newTree.subtree(nid))
                else:
                    newSubTree = mergeR(targetTree.subtree(nid), newTree.subtree(nid))
                    targetTree.remove_node(nid)
                    targetTree.paste(targetTree.root, newSubTree)

        def mergeR(lhs: SectionTree, rhs: SectionTree):
            mergedTree = SectionTree()
            mergedTree.addEntry(lhs._rootNode.data)
            # hopefully this method does not clean the tree

            safePaste(mergedTree, mergedTree.root, lhs)
            safePaste(mergedTree, mergedTree.root, rhs)

            return mergedTree

        return mergeR(self, otherTree)
