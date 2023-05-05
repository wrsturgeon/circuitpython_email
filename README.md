# Send Emails with CircuitPython

Modified from [this post](https://mjoldfield.com/atelier/2021/11/python-smtp.html)—please thank Martin Oldfield there instead of me!

## Setup
Write a `secrets.py` file in __the same folder as your main Python file__, formatted like this:
```python
secrets = {
    "email": "address@site.com",
    "password": "S3cureP@ssw0rd",
    "login_encrypted": "AGFkZHJlc3NAc2l0ZS5jb20AUzNjdXJlUEBzc3cwcmQ=" # See below the code snippet for an explanation!
    "host": "smtp.gmail.com",
    "port": 465, # Gmail's required SSL port
}
```

How did we get the value for `login_encrypted`?
In a terminal (not Python), type `echo -ne '\0{your username}\0{your password}' | base64`.
With the above email and password, it would be `echo -ne '\0address@site.com\0S3cureP@ssw0rd' | base64` (exactly, to the letter!), which should output `AGFkZHJlc3NAc2l0ZS5jb20AUzNjdXJlUEBzc3cwcmQ=`. Do this for your username and password, then copy it into the `login_encrypted` field.

## Use
e.g.
```python
from circuitpython_email import smtp
pool = socketpool.SocketPool(wifi.radio)
socket = pool.socket()
smtp.init_connection(socket)
smtp.send(
    socket=socket,
    to="destination@other.com",  # email ourselves!
    subject="Hello, World!",
    body="Hello from a CircuitPython device!",
)
```
