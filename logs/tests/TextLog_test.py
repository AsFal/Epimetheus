from unittest import TestCase

from logs import TextLog, Entry

from util import find

class TestTextLog(TestCase):
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
        self.child1 = Entry(self.LEVEL_ONE, self.L1_C1)
        self.child2 = Entry(self.LEVEL_ONE, self.L1_C2)
        self.child3 = Entry(self.LEVEL_ONE_PRIME, self.L1_C3)

        self.l2_child1 = Entry(self.LEVEL_TWO, self.L2_C1)
        self.l2_child2 = Entry(self.LEVEL_TWO, self.L2_C2)
        self.l2_child3 = Entry(self.LEVEL_TWO, self.L2_C3)
        mockTextLog = TextLog()
        self.root = mockTextLog._buildLogHeader()
        dummyText = '%s\n\t%s\n\t\t%s\n\t\t%s\n\t%s\n\t\t%s\n\t%s\n' % (
            self.root.toString(),
            self.child1.toString(),
            self.l2_child1.toString(),
            self.l2_child2.toString(),
            self.child2.toString(),
            self.l2_child3.toString(),
            self.child3.toString()
        )
        self.dummyTextLog = TextLog(oldLog=dummyText)

    def test_toTreeLog(self):
        print(self.dummyTextLog.getLogString())
        print(self.dummyTextLog.toTreeLog().getLogString())
        assert self.dummyTextLog.getLogString() == self.dummyTextLog.toTreeLog().getLogString()
