#!/usr/bin/env python3

import json
import curses
import requests

instructions = """nkodimote v0.1
Controls:
 - q     : Quit
 - w     : Up
 - a     : Left
 - s     : Down
 - d     : Right
 - b     : Back
 - h     : Home
 - enter : Select
 - space : Play/Pause (Hopefully)
 - ,     : seek backwards (short)
 - .     : seek forwards (short)
 - <     : seek backwards (long)
 - >     : seek forwards (long)
 - -     : voldown 1
 - =     : volup 1
 - _     : voldown 5
 - +     : volup 5
"""
url      = 'http://tk-oc1.local/jsonrpc'
headers  = {
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

def main(stdscr):
    stdscr.addstr(instructions)
    while True:
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
