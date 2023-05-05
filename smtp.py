# Code hugely inspired by https://mjoldfield.com/atelier/2021/11/python-smtp.html
# Don't thank me--vast majority of the credit goes to Martin Oldfield above!

# API lightly edited to power the Penn Center for Neuroaesthetics light sensor.

# Requires a `secrets.py` file--see the README.

import wifi
import socketpool

from secrets import secrets  # Your file!

host = secrets["host"]
port = secrets["port"]


# Inlining `smtplib.SMTP_SSL.login`:
# if not (200 <= self.ehlo()[0] <= 299):
#     (code, resp) = self.helo()
#     if not (200 <= code <= 299):
#         raise SMTPHeloError(code, resp)
# self.user, self.password = user, password
# for authmethod in ["CRAM-MD5", "PLAIN", "LOGIN"]:
#     method_name = "auth_" + authmethod.lower().replace("-", "_")
#     try:
#         (code, resp) = self.auth(
#             authmethod,
#             getattr(self, method_name),
#             initial_response_ok=initial_response_ok,
#         )
#         # 235 == 'Authentication successful'
#         # 503 == 'Error: already authenticated'
#         if code in (235, 503):
#             return (code, resp)
#     except SMTPAuthenticationError as e:
#         last_exception = e

# # We could not login successfully.  Return result of last attempt.
# raise last_exception


def init_connection(socket) -> None:
    """Connects to the `host` defined in `secrets.py`."""
    print("Connecting to", secrets["host"])
    addr = (secrets["host"], secrets["port"])
    socket.connect(addr)
    print("    done!")


def rxtx(s, msg):
    print("Talking to the SMTP server:")
    if msg is None:
        print("    [no data sent; waiting for the server to initiate]")
    else:
        print("    >>> " + msg)
        s.send(msg.encode("ascii") + b"\n")

    buff_size = 1024
    buff = bytearray(buff_size)
    s.recv_into(buff)
    x = buff.decode("ascii")
    print("    <<< " + x.rstrip())
    return x


def send(socket, to, subject, body):
    """Make sure to call `init_connection()` on `socket` at least once before!"""
    rxtx(socket, None)
    rxtx(socket, "HELO circuitpython_email")
    rxtx(socket, "MAIL FROM:{}".format(secrets["email"]))
    rxtx(socket, "RCPT TO:{}".format(to))
    rxtx(socket, "DATA")
    rxtx(
        socket,
        "From: {}\nTo: {}\nSubject: {}\n\n{}\n.".format(
            secrets["email"], to, subject, body
        ),
    )
