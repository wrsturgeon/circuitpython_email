# Code hugely inspired by https://mjoldfield.com/atelier/2021/11/python-smtp.html
# Don't thank me--vast majority of the credit goes to Martin Oldfield above!

# API lightly edited to power the Penn Center for Neuroaesthetics light sensor.

# Requires a `secrets.py` file--see the README.

from . import base64
import socketpool
import wifi

from secrets import secrets  # Your file!

host = secrets["host"]
port = secrets["port"]


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
    # Inlining `login` from `smtplib`:
    # for authmethod in ["CRAM-MD5", "PLAIN", "LOGIN"]:
    #     method_name = "AUTH_" + authmethod.replace("-", "_")
    #     try:
    #         # (code, resp) = self.auth(
    #         #     authmethod,
    #         #     getattr(self, method_name),
    #         #     initial_response_ok=initial_response_ok,
    #         # )
    #         authmethod = authmethod.upper()
    #         initial_response = (authobject() if initial_response_ok else None)
    #         if initial_response is not None:
    #             response = encode_base64(initial_response.encode('ascii'), eol='')
    #             (code, resp) = self.docmd("AUTH", authmethod + " " + response)
    #         else:
    #             (code, resp) = self.docmd("AUTH", authmethod)
    #         # If server responds with a challenge, send the response.
    #         if code == 334:
    #             challenge = base64.decodebytes(resp)
    #             response = encode_base64(
    #                 authobject(challenge).encode('ascii'), eol='')
    #             (code, resp) = self.docmd(response)
    #         if code in (235, 503):
    #             return (code, resp)
    #         raise SMTPAuthenticationError(code, resp)
    #         # 235 == 'Authentication successful'
    #         # 503 == 'Error: already authenticated'
    #         if code in (235, 503):
    #             return (code, resp)
    #     except SMTPAuthenticationError as e:
    #         last_exception = e
    # # We could not login successfully.  Return result of last attempt.
    # raise last_exception
    try:
        email = secrets["email"]
        password = secrets["password"]
        rxtx(socket, "AUTH PLAIN")
        rxtx(socket, base64.encode(email).decode('ascii'))
        rxtx(socket, base64.encode(password).decode('ascii'))
    except Exception as e:
        print(e)
        time.sleep(5)
        pass
    rxtx(socket, "MAIL FROM:{}".format(secrets["email"]))
    rxtx(socket, "RCPT TO:{}".format(to))
    rxtx(socket, "DATA")
    rxtx(
        socket,
        "From: {}\nTo: {}\nSubject: {}\n\n{}\n.".format(
            secrets["email"], to, subject, body
        ),
    )
