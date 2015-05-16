#!/usr/bin/env python3
import json
import socket
import curses

hostname = "tk-oc1.local"
port = 80

post_request = "POST /jsonrpc HTTP/1.1\r\nHost: {}\r\nUser-Agent: nkodimote/0.1\r\nContent-Type: application/json\r\nContent-Length: {}\r\n\r\n{}\r\n"

method_stub = '{{ "jsonrpc": "2.0", "method": "{}", "id": {} }}'

curr_id = 0

def call_rpc(method):
    global curr_id
    jsonrpc_call = method_stub.format(method, curr_id)
    curr_id += 1
    full_request = post_request.format(hostname, len(jsonrpc_call) + 2, jsonrpc_call)

    s.sendall(bytes(full_request, 'UTF-8'))

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
            if c == ord('w'):
                call_rpc("Input.Up")
            elif c == ord('a'):
                call_rpc("Input.Left")
            elif c == ord('s'):
                call_rpc("Input.Down")
            elif c == ord('d'):
                call_rpc("Input.Right")
            elif c == ord('b'):
                call_rpc("Input.Back")
            elif c == ord('h'):
                call_rpc("Input.Home")
            elif c == ord('r'):
                call_rpc("Input.Select")
            elif c == ord('q'):
                break

    except:
        pass

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()

    curses.endwin()
