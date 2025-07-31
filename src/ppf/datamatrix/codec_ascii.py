#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
datamatrix.ascii codec
++++++++++++++++++++++

Adds datamatrix.ascii codec to python's codecs.

encoded = 'ABC'.encode('datamatrix.ascii')
decoded = encoded.decode('datamatrix.ascii')

datamatrix.ascii is encoded as follows:

- digits: are encoded pairwise as 130 + numeric_value(pair)
  (e.g., '60' is encoded as 130 + 60 = 190).
  If there is only a single digit, it is encoded as ASCII(char) + 1.
- non-digit ASCII chars are encoded as ASCII(char) + 1
- extended ASCII chars: are currently not supported by ppf.datamatrix

.. author: Adrian Schlatter
"""
__all__ = []

import codecs


def encode(msg):
    """Encode to datamatrix.ascii."""
    enc = []
    length = len(msg)
    i = 0
    while i < length:
        c = msg[i]
        if c.isdigit() and i + 1 < length and msg[i + 1].isdigit():
            enc.append(130 + int(msg[i:i + 2]))
            i += 1
        elif ord(c) > 127:
            enc.append(235)
            enc.append((ord(c) - 127) & 255) 
        else:
            enc.append( ord(c) + 1)
        i += 1
    return bytes(enc), len(enc)


def decode(code):
    """Decode datamatrix.ascii-encoded message."""
    msg = ''
    length = len(code)
    i = 0
    while i < length:
        c = code[i]
        if 130 <= c and c < 230:
            msg += f'{c-130:02d}'
        elif c == 235:
            i += 1
            c = code[i]
            msg += chr(c+127)
        else:
            msg += chr(c-1)
        i += 1
    return msg, len(msg)


def search_codec(encoding_name):
    """Search function needed for registration in python codecs."""
    if encoding_name != 'datamatrix.ascii':
        return None

    return codecs.CodecInfo(encode,
                            decode,
                            name='datamatrix.ascii')


codecs.register(search_codec)
