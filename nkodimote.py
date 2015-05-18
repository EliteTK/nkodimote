#!/usr/bin/env python3

import json
import curses
import requests
from itertools import islice
import math

instructions = """nkodimote v0.1
Controls:
|[  q  ] Quit
|[  w  ] Up
|[  a  ] Left
|[  s  ] Down
|[  d  ] Right
|[  b  ] Back
|[  h  ] Home
|[enter] Select
|[space] Play/Pause
|[  ,  ] Seek Back (short)
|[  .  ] Seek Forw (short)
|[  <  ] Seek Back (long)
|[  >  ] Seek Forw (long)
|[  -  ] Voldown 1
|[  =  ] Volup 1
|[  _  ] Voldown 5
|[  +  ] Volup 5
"""

instructions_lines = instructions.split('\n')
instructions_height = len(instructions_lines)
instructions_width = 0

for line in instructions_lines:
    line_length = len(line)
    if instructions_width < line_length:
        instructions_width = line_length

instructions_width += 1

url     = 'http://tk-oc1.local/jsonrpc'
headers = {
    'User-Agent': 'nkodimote/0.1',
    'Content-Type': 'application/json'
}

curr_id = 0

actions_basic = {
    'w': ('Input.Up',),
    'a': ('Input.Left',),
    's': ('Input.Down',),
    'd': ('Input.Right',),
    'b': ('Input.Back',),
    'h': ('Input.Home',),
    '\n': ('Input.Select',),
    ' ': ('Player.PlayPause', 1),
    ',': ('Player.Seek', 1, 'smallbackward'),
    '.': ('Player.Seek', 1, 'smallforward'),
    '<': ('Player.Seek', 1, 'bigbackward'),
    '>': ('Player.Seek', 1, 'bigforward'),
}

actions_eval = {
    '-': 'volchg(-1)',
    '=': 'volchg( 1)',
    '_': 'volchg(-5)',
    '+': 'volchg( 5)'
}

def call_rpc(method, *params):
    global curr_id

    jsonrpc = {
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'id': curr_id
    }

    curr_id += 1

    r = requests.post(url, headers=headers, data=json.dumps(jsonrpc))

    return r.json()['result']

def volchg(amount):
    curr_vol = call_rpc('Application.GetProperties', ('volume', ))['volume']
    call_rpc('Application.SetVolume', curr_vol + amount)

def handle_key(key):
    try:
        call_rpc(*actions_basic[chr(key)])
    except KeyError:
        try:
            eval(actions_eval[chr(key)])
        except KeyError:
            pass

def print_col(stdscr, x, y, lineno, lines, width):
    for line in islice(instructions_lines, lineno, lineno + lines):
        stdscr.addnstr(y, x, line, width)
        y += 1

def print_instructions(stdscr):
    stdscr.clear()

    height, width = stdscr.getmaxyx()
    maxwidth = instructions_width
    maxheight = instructions_height

    cols = 1

    if width < instructions_width:
        maxwidth = width

    if height < instructions_height:
        maxheight = height
        cols = math.ceil(instructions_height / height)
        if maxwidth > int(width / cols):
            maxwidth = int(width / cols)

    stdscr.refresh()

    for col in range(cols):
        print_col(stdscr, col * maxwidth, 0, col * maxheight, maxheight, maxwidth)

def main(stdscr):
    while True:
        print_instructions(stdscr)
        c = stdscr.getch()
        if c == ord('q'):
            break
        else:
            try:
                handle_key(c)
            except KeyError:
                pass

if __name__ == '__main__':
    curses.wrapper(main)
