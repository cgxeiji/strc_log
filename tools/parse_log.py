import json
from termcolor import colored
import struct
import argparse
import sys

class Options:
    def __init__(self, log_level, show_origin):
        self.log_level = log_level
        self.show_origin = show_origin

    def __str__(self):
        return "log_level: {}, show_origin: {}".format(self.log_level, self.show_origin)


def load_json(filename):
    print("Loading file: {}".format(filename))
    with open(filename) as f:
        return json.load(f)

def get_str_from_id(database, id):
    if id >= len(database):
        return ""
    item = database[id]
    return item["string"]

def is_str_format(text, idx):
    found = 0
    for i in range(len(text)):
        if text[i] != "%":
            continue
        if i+1 >= len(text):
            return False
        if text[i+1] == "%":
            continue
        if text[i+1] == "s":
            if found == idx:
                return True
        found += 1
    return False

def read_stdin(database, options):
    while True:
        # read single byte
        byte = sys.stdin.buffer.read(database["strc_id_size"])
        if not byte:
            break
        id = int.from_bytes(byte, byteorder="little")
        strcs = database["string_constants"]
        if id < len(strcs):
            item = strcs[id]
            text = item["string"]
            marker = text.find(" | ")
            if marker != -1:
                if "in file: " in text:
                    marker += 3
                    if options.show_origin:
                        # make all text before | gray
                        text = colored(text[:marker], "white", attrs=["dark"]) + text[marker:]
                    else:
                        # delete all text before [
                        text = text[marker:]
            # make all text between % and any letter red
            a = text.split("%")
            got_empty = False
            for i in range(1, len(a)):
                # find index of first letter
                if (len(a[i]) == 0):
                    got_empty = True
                    a[i] = "%" + a[i]
                    continue
                if got_empty:
                    a[i] = "%" + a[i]
                    got_empty = False
                    continue

                idx = 0
                for j in range(0, len(a[i])):
                    if a[i][j].isalpha():
                        idx = j
                        break


                # replace % with red % and the rest of the string with red text
                a[i] = colored("%" + a[i][:idx+1], "cyan", attrs=[]) + a[i][idx+1:]
            text = "".join(a)

            
            log_level = 100
            if "[TRC]" in text:
                text = text.replace("[TRC]", colored("[TRC]", "white", attrs=["dark"]))
                log_level = 0
            if "[USR]" in text:
                text = text.replace("[USR]", colored("[USR]", "cyan", attrs=[]))
                log_level = 1
            if "[DBG]" in text:
                text = text.replace("[DBG]", colored("[DBG]", "green", attrs=[]))
                log_level = 2
            if "[INF]" in text:
                text = text.replace("[INF]", colored("[INF]", "green", attrs=["bold"]))
                log_level = 3
            if "[WRN]" in text:
                text = text.replace("[WRN]", colored("[WRN]", "yellow", attrs=["bold"]))
                log_level = 4
            if "[ERR]" in text:
                text = text.replace("[ERR]", colored("[ERR]", "red", attrs=["bold"]))
                log_level = 5
            if "[FTL]" in text:
                text = text.replace("[FTL]", colored("[FTL]", "red", attrs=["bold", "reverse"]))
                log_level = 6
            vars = item["variable_types"]
            variables = []
            for i in range(len(vars)):
                size = vars[i]["size"]
                byte = sys.stdin.buffer.read(size)
                if not byte:
                    break
                if "unsigned" in vars[i]["type"]:
                    if size == 1:
                        var = struct.unpack("<B", byte)[0]
                    elif size == 2:
                        var = struct.unpack("<H", byte)[0]
                    elif size == 4:
                        var = struct.unpack("<I", byte)[0]
                    else:
                        print("Unknown size: {}".format(size))
                    if is_str_format(text, i):
                        var = get_str_from_id(strcs, var)
                elif "char" in vars[i]["type"]:
                    var = struct.unpack("<c", byte)[0]
                elif "int" in vars[i]["type"]:
                    var = struct.unpack("<i", byte)[0]
                elif "float" in vars[i]["type"]:
                    var = struct.unpack("<f", byte)[0]
                elif "double" in vars[i]["type"]:
                    var = struct.unpack("<d", byte)[0]
                else:
                    print("Unknown type: {}".format(vars[i]["type"]))
                variables.append(var)

            formatted = text % tuple(variables)
            formatted = formatted.replace("%", colored("%", "cyan", attrs=[]))

            if log_level >= options.log_level:
                print(formatted)

def main():
    parser = argparse.ArgumentParser(description="Parse log stream")
    parser.add_argument("-d", "--database", help="string constant database")
    parser.add_argument("-s", "--show-origin", help="show origin of log message", action="store_true")
    parser.add_argument("-l", "--log-level", help="log level", default=3)
    database = parser.parse_args().database
    show_origin = parser.parse_args().show_origin
    log_level = int(parser.parse_args().log_level)

    database = load_json(database)
    read_stdin(database, Options(log_level, show_origin))


if __name__ == "__main__":
    main()
