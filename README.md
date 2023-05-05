# Send Emails with CircuitPython

Modified from [this post](https://mjoldfield.com/atelier/2021/11/python-smtp.html)—please thank Martin Oldfield there instead of me!

## Setup
Write a `secrets.py` file in __the same folder as your main Python file__, formatted like this:
```python
secrets = {
    "email": "address@site.com",
    "password": "S3cureP@ssw0rd",
    "host": "smtp.gmail.com",
    "port": 465, # Gmail's required SSL port
}
```

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
