from logs import SectionTree, Entry
from unittest import TestCase

from util import find

class TestSectionTree(TestCase):
    ROOT = "root"
    ROOT_MESSAGE ="rootMessage"
    LEVEL_ONE = "levelOne"
    LEVEL_ONE_PRIME = "levelOnePrime"
    L1_C1 = "l1c1"
    L1_C2 = "l1c2"
    L1_C3 = "l1c3"
    L1_C4 = "l1c4"
    LEVEL_TWO = "levelTwo"
    L2_C1 = "l2c1"
    L2_C2 = "l2c2"
    L2_C3 = "l2c3"
    L2_C4 = "l2c4"
    LEVEL_THREE = "levelThree"
    L3_C1 = "l3c1"
    L3_C2 = "l3c2"
    L3_C3 = "l3c3"
    L3_C4 = "l3c4"

    def setup_method(self, method):
        self.dummyTree = SectionTree()
        self.root = Entry(self.ROOT, self.ROOT_MESSAGE)
        self.dummyTree.addEntry(self.root)

        self.child1 = Entry(self.LEVEL_ONE, self.L1_C1)
        self.child2 = Entry(self.LEVEL_ONE, self.L1_C2)
        self.child3 = Entry(self.LEVEL_ONE_PRIME, self.L1_C3)
        self.dummyTree.addEntry(self.child1, self.root)
        self.dummyTree.addEntry(self.child2, self.root)
        self.dummyTree.addEntry(self.child3, self.root)

        self.l2_child1 = Entry(self.LEVEL_TWO, self.L2_C1)
        self.l2_child2 = Entry(self.LEVEL_TWO, self.L2_C2)
        self.l2_child3 = Entry(self.LEVEL_TWO, self.L2_C3)
        self.dummyTree.addEntry(self.l2_child1, self.child1)
        self.dummyTree.addEntry(self.l2_child2, self.child1)
        self.dummyTree.addEntry(self.l2_child3, self.child2)

    def test_toString(self):
        logString = '%s\n\t%s\n\t\t%s\n\t\t%s\n\t%s\n\t\t%s\n\t%s\n' % (
            self.root.toString(),
            self.child1.toString(),
            self.l2_child1.toString(),
            self.l2_child2.toString(),
            self.child2.toString(),
            self.l2_child3.toString(),
            self.child3.toString()
        )
        assert self.dummyTree.toString() == logString

    # tests for merge, toString and edit

    def test_merge(self):
        secondTree = SectionTree()
        secondTree.addEntry(self.root)
        secondTree.addEntry(self.child1, self.root)
        l2_child4 = Entry("l2_child4", "mhmmmm")
        secondTree.addEntry(l2_child4, self.child1)

        mergedTree = secondTree.merge(self.dummyTree)

        # Result should be
        # root
        #   child1
        #       l2_child1
        #       l2_child2
        #       l2_child4
        #   child2
        #       l2_child3
        #   child3

        def checkChildren(tree, nid, entries):
            assert len(tree[nid].fpointer) == len(entries)
            assert len([
                childNid for childNid in tree[nid].fpointer if tree[childNid].data.id not in [
                    entry.id for entry in entries
                ]
            ]) == 0

        def findChildNode(tree, parentNid, entry):
            return find(lambda nid: tree[nid].data.id == entry.id, tree[parentNid].fpointer)

        checkChildren(mergedTree, mergedTree.root, [self.child1, self.child2, self.child3])

        child1Nid = findChildNode(mergedTree, mergedTree.root, self.child1)
        checkChildren(mergedTree, child1Nid, [self.l2_child1, self.l2_child2, l2_child4])
        child2Nid = findChildNode(mergedTree, mergedTree.root, self.child2)
        checkChildren(mergedTree, child2Nid, [self.l2_child3])
        child3Nid = findChildNode(mergedTree, mergedTree.root, self.child3)
        checkChildren(mergedTree, child3Nid, [])

    def test_edit(self):
        assert 1 == 1
