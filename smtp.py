# Code hugely inspired by https://mjoldfield.com/atelier/2021/11/python-smtp.html
# Don't thank me--vast majority of the credit goes to Martin Oldfield above!

# API lightly edited to power the Penn Center for Neuroaesthetics light sensor.

# Requires a `secrets.py` file--see the README.

import time
import wifi
import socketpool

from secrets import secrets


def mail_open_socket():
    server = secrets["smtp_server"]
    print("Connecting to mail server ", server)
    pool = socketpool.SocketPool(wifi.radio)
    sock = pool.socket()
    addr = (server, 25)
    sock.connect(addr)
    return sock


def mail_rxtx(s, msg):
    if msg is not None:
        print("> " + msg)
        s.send(msg.encode("ascii") + b"\n")

    buff_size = 1024
    buff = bytearray(buff_size)
    s.recv_into(buff)
    x = buff.decode("ascii")
    print("< " + x.rstrip())
    return x


def mail_send(m_subj, m_msg):
    m_from = secrets["mail_from"]
    m_to = secrets["mail_to"]

    s = mail_open_socket()
    mail_rxtx(s, None)
    mail_rxtx(s, "HELO pico")
    mail_rxtx(s, "MAIL FROM:{}".format(m_from))
    mail_rxtx(s, "RCPT TO:{}".format(m_to))
    mail_rxtx(s, "DATA")
    mail_rxtx(
        s, "From: {}\nTo: {}\nSubject: {}\n\n{}\n.".format(m_from, m_to, m_subj, m_msg)
    )


print("connect to wifi")
wifi_connect()
time.sleep(sleep_time)

print("Send email")
m_subj = "Hello World!"
m_msg = "Your text goes here"
mail_send(m_subj, m_msg)
