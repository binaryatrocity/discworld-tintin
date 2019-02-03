#!/usr/bin/env python

import os
import re
import sys
import math
import json


class MapDoorText:
    number_map = {
        "a ": 1,
        "an ": 1,
        "the ": 1,
        "one ": 1,
        "two ": 2,
        "three ": 3,
        "four ": 4,
        "five ": 5,
        "six ": 6,
        "seven ": 7,
        "eight ": 8,
        "nine ": 9,
        "ten ": 10,
        "eleven ": 11,
        "twelve ": 12,
        "thirteen ": 13,
        "fourteen ": 14,
        "fifteen ": 15,
        "sixteen ": 16,
        "seventeen ": 17,
        "eighteen ": 18,
        "nineteen ": 19,
        "twenty ": 20,
        "twenty-one ": 21,
        "twenty-two ": 22,
        "twenty-three ": 23,
        "twenty-four ": 24,
        "twenty-five ": 25,
        "twenty-six ": 26,
        "twenty-seven ": 27,
        "twenty-eight ": 28,
        "twenty-nine ": 29,
        "thirty ": 30,
    }

    direction_map = {
        "north": "n",
        "northeast": "ne",
        "east": "e",
        "southeast": "se",
        "south": "s",
        "southwest": "sw",
        "west": "w",
        "northwest": "nw",
        "n": "n",
        "ne": "ne",
        "e": "e",
        "se": "se",
        "s": "s",
        "sw": "sw",
        "w": "w",
        "nw": "nw",
    }
    colour_map = {
        # http://terminal-color-builder.mudasobwa.ru/
        "orange": "\033[01;38;05;214m",
        "red": "\033[01;38;05;196m",
        "cyan": "\033[01;38;05;37m",
        "reset":  "\033[00;39;49m"
    }

    def __init__(self):
        self.return_value = []
        self.custom_matches = []

        # Load the JSON configuration file
        with open('mdtconfig.json', 'r') as config_file:
            config = json.load(config_file)

        # Strip comments from custom matches
        for match in config['custom_matches']:
            if len(match) > 1:
                self.custom_matches.append(match)

        self.default_npc_value = config['default_npc_value']
        self.bonus_player_value = config['bonus_player_value']
        self.minimum_room_value = config['minimum_room_value']
        self.show_hidden_room_count = config['show_hidden_room_count']

    @staticmethod
    def explode(div, mdt):
        if div == '':
            return False
        pos, fragments = 0, []
        for m in re.finditer(div, mdt):
            fragments.append(mdt[pos:m.start()])
            pos = m.end()
        fragments.append(mdt[pos:])
        return fragments

    def parse_mdt(self, mdt_line):
        # Make lower case, do initial replacements
        mdt_line = mdt_line.lower()
        mdt_line = mdt_line.replace(" are ", " is ")
        mdt_line = mdt_line.replace(" black and white ", " black white ")
        mdt_line = mdt_line.replace(" brown and white ", " brown white ")
        mdt_line = mdt_line.replace("the limit of your vision is ", "the limit of your vision:")
        mdt_line = mdt_line.replace(" and ", ", ")
        mdt_line = mdt_line.replace(" is ", ", ")
        mdt_table = self.explode(', ', mdt_line)

        data = {
            'last_direction': '',
            'last_enemy_line': '',
            'last_count': 0,
            'last_was_dir': 0,
            'enemies_by_square': [],
            'ignoring_exits': False,
            'entity_table': [],
            'room_id': 1,
            'room_value': 0,
            'longest_direction': 0,
            'nothing': True,
            'next_color': ''
        }
        exit_strings = ['doors ', 'a door ', 'exits ', 'an exit ', 'a hard to see through exit ']

        for entry in mdt_table:
            if entry != "" and ' of a ' not in entry:
                if entry.startswith(tuple(exit_strings)):
                    # print('Special exit, ignore this line? next line is processed...')
                    data['ignoring_exits'] = True
                elif entry.startswith('the limit of your vision:'):
                    if data['last_count'] > 0:
                        this_square = [data['last_count'], data['last_direction'], data['room_id'], int(math.floor(data['room_value']))]
                        data['enemies_by_square'].append(this_square)
                        data['nothing'] = False
                        data['next_color'] = ''
                        data['room_id'] = data['room_id'] + 1
                        data['room_value'] = 0
                    data['last_direction'] = ''
                    data['last_enemy_line'] = ''
                    data['last_count'] = 0
                    data['last_was_dir'] = 0
                else:
                    # find the quantity first
                    quantity = 1
                    for nm_key in self.number_map:
                        if entry.startswith(nm_key):
                            quantity = self.number_map[nm_key]
                            entry = entry[len(nm_key):]
                            break

                    is_direction = 0
                    this_direction = ''

                    if entry.startswith("northeast"):
                        is_direction = 1
                        this_direction = "northeast"
                    elif entry.startswith("northwest"):
                        is_direction = 1
                        this_direction = "northwest"
                    elif entry.startswith("southeast"):
                        is_direction = 1
                        this_direction = "southeast"
                    elif entry.startswith("southwest"):
                        is_direction = 1
                        this_direction = "southwest"
                    elif entry.startswith("north"):
                        is_direction = 1
                        this_direction = "north"
                    elif entry.startswith("east"):
                        is_direction = 1
                        this_direction = "east"
                    elif entry.startswith("south"):
                        is_direction = 1
                        this_direction = "south"
                    elif entry.startswith("west"):
                        is_direction = 1
                        this_direction = "west"

                    if is_direction == 1:
                        if not data['ignoring_exits']:
                            # print('[handling direction, not exits]')
                            data['last_was_dir'] = 1

                            if data['last_direction'] != '':
                                data['last_direction'] = '{}, '.format(data['last_direction'])
                        
                            data['last_direction'] = '{}{} {}'.format(
                                data['last_direction'], quantity, self.direction_map[this_direction]
                            )
                        else:
                            # print('[ignoring exits direction line]')
                            pass
                    else:
                        data['ignoring_exits'] = False
                        if data['last_was_dir'] == 1:
                            # reset count
                            if data['last_count'] > 0:
                                this_square = [data['last_count'], data['last_direction'], data['room_id'], int(math.floor(data['room_value']))]
                                data['enemies_by_square'].append(this_square)
                                data['nothing'] = False
                                data['next_color'] = ''
                                data['room_id'] = data['room_id'] + 1
                                data['room_value'] = 0
                            data['last_direction'] = ''
                            data['last_enemy_line'] = ''
                            data['last_count'] = 0
                            data['last_was_dir'] = 0

                        data['next_color'] = ''
                        add_player_value = False

                        # Special GMCP MDT colour codes
                        if entry[0:6] == 'u001b[':
                            # u001b[38;5;37mRuhsbaaru001b[39;49mu001b[0m
                            here = entry.index('m')
                            data['next_color'] = entry[7:here]
                            # entry = entry[here + 1:-20]
                            # entry = entry.replace('u001b', '')
                            entry = entry.replace('u001b', '\033')

                            # Might be a second colour code for PK
                            if entry[0:6] == 'u001b[':
                                here = entry.index('m')
                                data['next_color'] = entry[7:here]
                                entry = entry[here + 1:-20]
                            add_player_value = True

                        this_value = self.default_npc_value

                        for custom_match in self.custom_matches:
                            if custom_match[3]:
                                # This is a regex match
                                rexp = re.compile(custom_match[0])
                                if rexp.match(entry):
                                    if custom_match[1] and custom_match[1] in self.colour_map:
                                        entry = '{}{}{}'.format(
                                            self.colour_map[custom_match[1]],
                                            entry,
                                            self.colour_map['reset']
                                        )
                                    this_value = custom_match[2]
                            else:
                                # This is a regular string match
                                if custom_match[0] in entry:
                                    if custom_match[1] and custom_match[1] in self.colour_map:
                                        entry = '{}{}{}'.format(
                                            self.colour_map[custom_match[1]],
                                            entry,
                                            self.colour_map['reset']
                                        )

                                    this_value = custom_match[2]

                        if add_player_value == True:
                            this_value = this_value + self.bonus_player_value

                        data['room_value'] = data['room_value'] + (this_value * quantity)

                        if quantity > 1:
                            entry = '{} {}'.format(quantity, entry)
                        data['entity_table'].append([data['room_id'], entry, data['next_color']])

                        data['last_count'] = data['last_count'] + quantity
                        if data['last_enemy_line'] != '':
                            data['last_enemy_line'] = '{}, '.format(data['last_enemy_line'])
                        data['last_enemy_line'] = '{}{}'.format(data['last_enemy_line'], entry)

        if data['nothing']:
            self.return_value.append('Nothing seen, try elsewhere!')
        else:
            done_here = False
            rooms_ignored = 0

            data['enemies_by_square'].sort(key=lambda square: square[3])

            # Grab shortest
            for square in data['enemies_by_square']:
                # Only show if this room meets the minimum value
                if square[3] >= self.minimum_room_value and len(square[1]) > data['longest_direction']:
                    data['longest_direction'] = len(square[1])

            for square in data['enemies_by_square']:
                # Only show if this room meets the minimum value
                if square[3] >= self.minimum_room_value:
                    done_here = False

                    # add colour to points output
                    square[3] = '{}{}{}'.format(self.colour_map['cyan'], square[3], self.colour_map['reset'])
                    fstring = '{{:<{}}} [{{}}] '.format(data['longest_direction'])
                    output = fstring.format(square[1], square[3])
                    for entity in data['entity_table']:
                        if entity[0] == square[2]:
                            if done_here:
                                output = '{}, '.format(output)
                            output = '{}{}'.format(output, entity[1])
                            done_here = True
                    if square[0] < 2:
                        output = '{} [{} thing]'.format(output, square[0])
                    else:
                        output = '{} [{} things]'.format(output, square[0])
                    self.return_value.append(output)
                else:
                    rooms_ignored = rooms_ignored + 1

                square = None

            for entity in data['entity_table']:
                entity = None

            if rooms_ignored > 0 and self.show_hidden_room_count:
                output = '({} rooms below your value limit of {})'.format(rooms_ignored, self.minimum_room_value)
                self.return_value.append(output)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('[error] No input provided.')
        sys.exit()

    argument, mdt_line = sys.argv.pop(1), None

    # Is this a file passed to us?
    if os.path.exists(argument):
        with open(argument, 'r') as f:
            mdt_line = f.readline()

    else:
        mdt_line = argument

    mdt = MapDoorText()
    mdt.parse_mdt(mdt_line)

    for line in mdt.return_value:
        print(line)
