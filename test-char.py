from getch import getch

from interface import suggestiveInput

def orderChecker():
    while True:
        c = getch()
        if ord(c) == 10:
            break
        else:
            print("Char: %s, Order: %s" % (c, ord(c)))

def suggestionsTest():
    availableWords = [
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
    finalWord = suggestiveInput(availableWords)
    print("|===%s===|" % finalWord)


def main():
    # orderChecker()
    suggestionsTest()

main()