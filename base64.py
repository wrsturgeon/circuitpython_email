# almost a copy of https://gist.github.com/trondhumbor/ce57c0c2816bb45a8fbb
# all credit to the above

CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def b64_chunk(data, length):
    return [data[i : i + length] for i in range(0, len(data), length)]


def b64_encode(bytes):
    print("AAAAA")
    override = 0
    if len(bytes) % 3 != 0:
        override = (len(bytes) + 3 - len(bytes) % 3) - len(bytes)
    bytes += b"\x00" * override

    print("BBBBB")
    threechunks = b64_chunk(bytes, 3)

    print("CCCCC")
    binstring = ""
    for chunk in threechunks:
        for x in chunk:
            binstring += "{:0>8}".format(bin(x)[2:])

    print("DDDDD")
    sixchunks = b64_chunk(binstring, 6)

    print("EEEEE")
    outstring = ""
    for element in sixchunks:
        outstring += CHARS[int(element, 2)]

    print("FFFFF")
    outstring = outstring[:-override] + "=" * override
    return outstring


def b64_decode(data):
    override = data.count("=")
    data = data.replace("=", "A")

    binstring = ""
    for char in data:
        binstring += "{:0>6b}".format(self.CHARS.index(char))

    eightchunks = b64_chunk(binstring, 8)

    outbytes = b""
    for chunk in eightchunks:
        outbytes += bytes([int(chunk, 2)])

    return outbytes[:-override]
