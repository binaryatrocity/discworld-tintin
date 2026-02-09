#!/usr/bin/env python

import re
import sys
import json


class MapDoorTextControl:
    colour_map = {
        # http://terminal-color-builder.mudasobwa.ru/
        "orange": "\033[01;38;05;214m",
        "red": "\033[01;38;05;196m",
        "cyan": "\033[01;38;05;37m",
        "reset":  "\033[00;39;49m"
    }

    def __init__(self):
        self.custom_matches = []

        # Load any additional custom matches
        with open('logs/features/mdt_custom_matches.json', 'r') as custom_file:
            config = json.load(custom_file)

        # Strip comments from custom matches
        for match in config:
            if len(match) > 1:
                self.custom_matches.append(match)

    def _write_file(self):
        with open('logs/features/mdt_custom_matches.json', 'w') as custom_file:
            json.dump(self.custom_matches, custom_file)

    def add_match(self, pattern, color="red", value=5, is_regex=False):
        self.custom_matches.append([pattern, color, value, is_regex])
        self._write_file()

    def remove_match(self, pattern):
        for match in self.custom_matches:
            if match[0] == pattern or pattern in match[0]:
                self.custom_matches.remove(match)
        self._write_file()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        #print('[error] Missing inputs. Usage: mdt_matchcontrol.py <command> <pattern>')
        print(0)
        sys.exit()

    script, command, pattern = sys.argv.pop(0), sys.argv.pop(0), " ".join(sys.argv)

    mdtc = MapDoorTextControl()
    if command == "add":
        mdtc.add_match(pattern)
        print(1)
    elif command == "remove":
        mdtc.remove_match(pattern)
        print(1)
    else:
        #print('[error] Unrecognized command, valid commands are "add" and "remove".')
        print(0)
