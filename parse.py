import re
import token

INDENTATION = 3

# creates XML representation of the matched token
def parse(token, text, spacing = 0):
    pos = 0
    print(" " * spacing, token.open_tag)

    # if non-terminal
    if token.children:
        for child in token.children:
            compiled = re.compile(child.regex)
            match = compiled.search(text, pos)
            spacing += INDENTATION
            parse(child, match.group(0), spacing)
            pos = match.end()
            spacing -= INDENTATION
    # if terminal
    else:
        print(" " * spacing, text)
    print(" " * spacing, token.closed_tag)
