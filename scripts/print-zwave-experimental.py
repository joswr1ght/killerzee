#!/usr/bin/env python

import sys
import binascii
import signal
import traceback

from rflib import *

PREAMBLE="01"*8
SFD="11110000"

# "\x00\x7a\x74\x9d\xef\x41\x00\x0c\x01\x27\x04" CHK=0xec
# "\x00\x7a\x74\x9d\xef\x41\x00\x0c\x01\x27\x05" CHK=0xed

def calcchksum(mpdu):
    checksum = 0xff
    for i in range(len(mpdu)):
        checksum ^= ord(mpdu[i])
    return checksum

def str_to_binary(s):
    return ''.join(['%08d'%int(bin(ord(i))[2:]) for i in s])

# Assumes first bit is starting (no leading 0 suppression)
def binary_to_hex(b):
    sb = (b[i:i+8] for i in range(0, len(b), 8)) # 8-bit blocks
    return ''.join(chr(int(char, 2)) for char in sb)

def hexdump(s):
    return ":".join(x.encode('hex') for x in s)

def sighandler(signal, frame):
    global sigstop
    sigstop=1

if __name__ == "__main__":
    sigstop=0
    if len(sys.argv) > 1:
        pktflen = int(sys.argv[1])
        if pktflen > 54:
            print "Packet length too long, cannot exceed 54 bytes."
            sys.exit(1)
        if pktflen < 9:
            print "Packet length too short, cannot be less than 9 bytes."
            sys.exit(1)
    else:
        print "Usage: %s [pktlen]"%sys.argv[0]
        sys.exit(0)


    d = RfCat(0, debug=False)
    d.setFreq(908419830)
    d.setMdmModulation(MOD_2FSK)
    d.setMdmSyncWord(0x55f0)
    d.setMdmDeviatn(19042.969)
    d.setMdmChanSpc(199951.172)
    d.setMdmChanBW(101562.5)
    d.setMdmDRate(19191.7)
    d.makePktFLEN(pktflen)
    d.setEnableMdmManchester(True)
    d.setMdmSyncMode(SYNCM_CARRIER)
    #d.setMdmSyncMode(SYNCM_CARRIER_15_of_16)

    signal.signal(signal.SIGINT, sighandler)
    while(not sigstop):
        try:
            packet = d.RFrecv()[0] # Just the data, no timestamp
            print hexdump(packet)
        except ChipconUsbTimeoutException:
            continue

