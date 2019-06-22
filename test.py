# CONFIG_FILENAME = "config0.bnf"
# file = open(CONFIG_FILENAME)
# lines = file.readlines()
# for line in lines:
#     arr = line.split(" ::= ")
#     print(arr[0])

# name = "<token>"
# print(name[1:-1])

#
# str = "a|b|c"
# arr = str.split("|")
# for item in arr:
#     print(item)

class Foo:
    def __init__(self):
        self.data = 1



dict = {}
foo = Foo()
dict[foo] = 1
dict[foo] = 2

for key in dict:
    print(key, dict[key])
