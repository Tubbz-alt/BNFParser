def clear_file(filename):
    file = open(filename, 'w')
    file.write("")
    file.close()