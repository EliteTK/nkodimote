#!/usr/bin/env python3

import json
import curses
import requests

url      = "http://tk-oc1.local/jsonrpc"
headers  = {
    'User-Agent': 'nkodimote/0.1',
    'Content-Type': 'application/json'
}

curr_id = 0

actions = {
    "w": ("Input.Up",               ),
    "a": ("Input.Left",             ),
    "s": ("Input.Down",             ),
    "d": ("Input.Right",            ),
    "b": ("Input.Back",             ),
    "h": ("Input.Home",             ),
    "r": ("Input.Select",           ),
    " ": ("Player.PlayPause",      1),
    "p": ("Player.GetActivePlayers",)
}

def call_rpc(method, *params):
    global curr_id
    jsonrpc = {
        'jsonrpc': '2.0',
        'method' : method,
        'params' : params,
        'id'     : curr_id
    }
    curr_id += 1

    r = requests.post(url, headers=headers, data=json.dumps(jsonrpc))

    return r.json()

def main(stdscr):
    try:
        while True:
            c = stdscr.getch()
            if c == ord('q'):
                break
            else:
                try:
                    call_rpc(*actions[chr(c)])
                except KeyError:
                    pass

    except Exception as e:
        raise e

if __name__ == "__main__":
    curses.wrapper(main)
