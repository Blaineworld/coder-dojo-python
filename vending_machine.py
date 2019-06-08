
_total = 100.0
_selections = {
    "A1": ("peanuts", .5),
    "A2": ("chips", .75),
    "A3": ("cookies", 1.0),
    "B1": ("gum", .25),
    "B2": ("trail mix", 1.5),
    "B3": ("20oz soda", 1.25),
    "C1": ("crazy expensive item", 99.0)
}

def greet():
    print("Welcome!\n")


def display_items():
    for (k, v) in _selections.items():
        print("{0}) {1[0]:.<30}${1[1]:,.2f}".format(k, v))


def prompt_selection():
    invalid = True
    while invalid:
        selected = input("Please make a selection. -- (Current balance: ${:,.2f})\n".format(_total))
        invalid = selected.lower() not in [k.lower()
                                           for k, v in _selections.items()]
        if invalid:
            print("Invalid selection...")
    return selected.upper()


def handle_purchase(selection):
    global _total
    item = _selections[selection]
    if _total >= item[1]:
        _total -= item[1]
        print("Here's your {}!".format(item[0]))
        print("Your remaining balance is ${0:,.2f}".format(_total))
        return True
    else:
        print("Sorry, you only have ${0:,.2f}".format(_total, item[1]))
        return False

def prompt_repeat(purchased):
    invalid = True
    question = "Would you like to make another purchase?" if purchased else "Would you like to buy something else?"
    while invalid:
        selected = input("{} (y, yes, n, no)\n".format(question))
        invalid = selected.lower() not in ['y','yes','n','no']
        if invalid:
            print("""Invalid input...
            Please enter one of: y, yes, n, no
            """)
    return selected in ['n','no']

if __name__ == "__main__":
    greet()
    quit = False
    while not quit:
        display_items()
        selection = prompt_selection()
        purchased = handle_purchase(selection)
        quit = prompt_repeat(purchased)
    print("Thank you!")
