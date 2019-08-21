from getch import getch

from interface import suggestiveEntry


def orderChecker():
    while True:
        c = getch()
        if ord(c) == 10:
            break
        else:
            print("Char: %s, Order: %s" % (c, ord(c)))

def suggestionsTest():
    availableEntries = [
        "Alex",
        "Alexandre",
        "Animation",
        "Ale"
        "Alement",
        "Abheration",
        "Acne",
        "Adandos",
        "Afilliation"
    ]
    availableTitles = [
        "Cat1",
        "Cat2",
        "Cat3"
    ]
    entry = suggestiveEntry(availableTitles, availableEntries)
    print("Final log")
    print("%s: %s" % (entry[0], entry[1]))


def main():
    # orderChecker()
    print("Start")
    suggestionsTest()

main()