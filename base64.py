# almost a copy of https://gist.github.com/trondhumbor/ce57c0c2816bb45a8fbb
# all credit to the above

CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def chunk(data, length):
    return [data[i : i + length] for i in range(0, len(data), length)]


def encode(data):
    print("AAAAA")
    override = 0
    print("AAAAB")
    if len(data) % 3 != 0:
        print("AAAAC")
        override = (len(data) + 3 - len(data) % 3) - len(data)
        print("AAAAD")
    print("AAAAE")
    data += b"\x00" * override
    print("AAAAF")

    print("BBBBB")
    threechunks = chunk(data, 3)

    print("CCCCC")
    binstring = ""
    for chunk in threechunks:
        for x in chunk:
            binstring += "{:0>8}".format(bin(x)[2:])

    print("DDDDD")
    sixchunks = chunk(binstring, 6)

    print("EEEEE")
    outstring = ""
    for element in sixchunks:
        outstring += CHARS[int(element, 2)]

    print("FFFFF")
    outstring = outstring[:-override] + "=" * override
    return outstring


def decode(data):
    override = data.count("=")
    data = data.replace("=", "A")

    binstring = ""
    for char in data:
        binstring += "{:0>6b}".format(self.CHARS.index(char))

    eightchunks = chunk(binstring, 8)

    outbytes = b""
    for chunk in eightchunks:
        outbytes += bytes([int(chunk, 2)])

    return outbytes[:-override]


if __name__ == "__main__":
    b64 = Base64()
    print(b64.decode(b64.encode(b"Hello")))
