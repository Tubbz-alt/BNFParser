CONFIG_FILENAME = "resources\\config.bnf"
EXT_CONFIG_FILENAME = "resources\\config_final.bnf"
CITIES_FILENAME = "resources\\veliki_gradovi.csv"
INDENTATION = 3


def copy_init_config():
    with open(CONFIG_FILENAME) as in_file, open(EXT_CONFIG_FILENAME, 'w') as out_file:
        out_file.write("")
        lines = in_file.readlines()
        for line in lines:
            out_file.write(line)