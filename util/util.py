def isEmpty(string):
    return string == ""

def flatten(l):
    return [item for sublist in l for item in sublist]

def isWhitespace(string):
    if isEmpty(string):
        return True
    if string[0] != " " or string[0] != "\t":
        return False
    return isWhitespace(string[1:])

def countTabs(line):
    def countTabsR(line, count):
        if isEmpty(line):
            return count
        if line[0] == "\t":
            return countTabsR(line[1:], count + 1)
        return count
    return countTabsR(line, 0)

