import re
import token
import parse


text = "111-A222 B57 111A222"                   # sample text
CONFIG_FILENAME = "config0.bnf"
file = open(CONFIG_FILENAME)
lines = file.readlines()
root = token.tokenize(lines)

# searches for root matches line by line
compiled = re.compile(root.regex)
pos = 0
while compiled.search(text, pos):
    match = compiled.search(text, pos)
    parse.parse(root, match.group(0))
    print("----------------------------------")
    pos = match.end()
