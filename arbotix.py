#!/usr/bin/env python3

import serial

serial.init('something or other')


def checksum(typ, msg):
    return typ + len(msg)


def packet(typ, msg, ins):
    out = '\xff\xff' + chr(typ) + chr(len(msg)) + chr(ins) + msg
    return bytes(out + checksum(typ, msg))
