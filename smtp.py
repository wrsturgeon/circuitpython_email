# Code hugely inspired by https://mjoldfield.com/atelier/2021/11/python-smtp.html
# Don't thank me--vast majority of the credit goes to Martin Oldfield above!

# API lightly edited to power the Penn Center for Neuroaesthetics light sensor.

# Requires a `secrets.py` file--see the README.

import wifi
import socketpool

from secrets import secrets  # Your file!

host = secrets["host"]
port = secrets["port"]


def init_connection():
    print("Connecting to", secrets["host"])
    socket = socketpool.SocketPool(wifi.radio).socket()
    addr = (secrets["host"], secrets["port"])
    socket.connect(addr)
    print("    done!")
    return socket


def rxtx(s, msg):
    if msg is not None:
        print("> " + msg)
        s.send(msg.encode("ascii") + b"\n")

    buff_size = 1024
    buff = bytearray(buff_size)
    s.recv_into(buff)
    x = buff.decode("ascii")
    print("< " + x.rstrip())
    return x


def send(to, subject, body):
    socket = init_connection()
    rxtx(socket, None)
    rxtx(socket, "HELO pico")
    rxtx(socket, "MAIL FROM:{}".format(secrets["email"]))
    rxtx(socket, "RCPT TO:{}".format(to))
    rxtx(socket, "DATA")
    rxtx(
        socket,
        "From: {}\nTo: {}\nSubject: {}\n\n{}\n.".format(
            secrets["email"], to, subject, body
        ),
    )
