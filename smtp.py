# Code hugely inspired by https://mjoldfield.com/atelier/2021/11/python-smtp.html
# Don't thank me--vast majority of the credit goes to Martin Oldfield above!

# API lightly edited to power the Penn Center for Neuroaesthetics light sensor.

# Requires a `secrets.py` file--see the README.

import wifi
import socketpool
import ssl
import sys

from secrets import secrets  # Your file!
host = secrets["host"]
port = secrets["port"]


context = ssl.create_default_context()
# with smtplib.SMTP_SSL(host=host, port=port, context=context) as server:
# ==> smtplib.SMTP.__init__(self, host, port, local_hostname, timeout, source_address)
# ==>
# (code, msg) = self.connect(secrets["host"], secrets["port"])
# self.sock = self._get_socket(host, port, self.timeout)
# (code, msg) = self.getreply()
# if code != 220:
#     self.close()
#     raise SMTPConnectError(code, msg)
# # RFC 2821 says we should use the fqdn in the EHLO/HELO verb, and
# # if that can't be calculated, that we should use a domain literal
# # instead (essentially an encoded IP address like [A.B.C.D]).
# fqdn = socket.getfqdn()
# if '.' in fqdn:
#     self.local_hostname = fqdn
# else:
#     # We can't find an fqdn hostname, so use a domain literal
#     addr = '127.0.0.1'
#     try:
#         addr = socket.gethostbyname(socket.gethostname())
#     except socket.gaierror:
#         pass
#     self.local_hostname = '[%s]' % addr



def mail_open_socket():
    print("Connecting to", secrets["host"])
    pool = socketpool.SocketPool(wifi.radio)
    socket = pool.socket()
    addr = (secrets["host"], 25)
    response = socket.connect(addr)
    print(response)
    return socket


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


def mail_send(to, subject, body):
    socket = mail_open_socket()
    mail_rxtx(socket, None)
    mail_rxtx(socket, "HELO pico")
    mail_rxtx(socket, "MAIL FROM:{}".format(secrets["email"]))
    mail_rxtx(socket, "RCPT TO:{}".format(to))
    mail_rxtx(socket, "DATA")
    mail_rxtx(
        socket,
        "From: {}\nTo: {}\nSubject: {}\n\n{}\n.".format(
            secrets["email"], to, subject, body
        ),
    )


mail_send(
    to=secrets["email"],  # email ourselves!
    subject="Hello, World!",
    body="Hello from your CircuitPython device!",
)
