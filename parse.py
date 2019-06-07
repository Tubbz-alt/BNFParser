import re
import symbol

INDENTATION = 3

# creates XML representation of the matched symbol
def parse(symbol, text, spacing = 0):
    pos = 0
    print(" " * spacing, symbol.open_tag)

    # if non-terminal
    if symbol.children:
        for child in symbol.children:
            compiled = re.compile(child.regex)
            match = compiled.search(text, pos)
            spacing += INDENTATION
            parse(child, match.group(0), spacing)
            pos = match.end()
            spacing -= INDENTATION

    # if terminal
    else:
        print(" " * spacing, text)

    print(" " * spacing, symbol.closed_tag)
