#!/usr/bin/env python3
import json
import socket
import curses

hostname = "tk-oc1.local"
port = 80

post_request = "POST /jsonrpc HTTP/1.1\r\nHost: {}\r\nUser-Agent: nkodimote/0.1\r\nContent-Type: application/json\r\nContent-Length: {}\r\n\r\n{}\r\n"

method_stub        = '{{ "jsonrpc": "2.0", "method": "{}", "id": {} }}'
method_stub_params = '{{ "jsonrpc": "2.0", "method": "{}", "params": [{}], "id": {} }}'

curr_id = 0

actions = {
    "w": ("Input.Up",                None),
    "a": ("Input.Left",              None),
    "s": ("Input.Down",              None),
    "d": ("Input.Right",             None),
    "b": ("Input.Back",              None),
    "h": ("Input.Home",              None),
    "r": ("Input.Select",            None),
    " ": ("Player.PlayPause",        "1"),
    "p": ("Player.GetActivePlayers", None)
}

def call_rpc(method, params = None):
    global curr_id

    if params is None:
        jsonrpc_call = method_stub.format(method, curr_id)
    else:
        jsonrpc_call = method_stub_params.format(method, params, curr_id)

    full_request = post_request.format(hostname, len(jsonrpc_call) + 2, jsonrpc_call)

    curr_id += 1
    s.sendall(bytes(full_request, 'UTF-8'))
    #print(s.recv(2048).decode('UTF-8'))

if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((socket.gethostbyname(hostname), port))
        #s.setblocking(False)

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
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()

        curses.endwin()

        raise e

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()

    curses.endwin()
