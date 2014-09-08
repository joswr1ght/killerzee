from pcapdump import *
from pcapdlt import *
from kzutils import *
from kzdecode import *
from rflib import *
from struct import *
import time

RFPROFILE_R1 = 0
RFPROFILE_R2 = 1
RFPROFILE_R3 = 2

# FCS calculation is 1 byte, same for R1 and R2
def calcfcs_r1(packet):
    checksum = 0xff
    for i in range(len(packet)):
        checksum ^= ord(packet[i])
    return checksum

def calcfcs_r2(packet):
    return calcfcs_r1(packet)


# FCS calculation is 2 bytes
def calcfcs_r3(packet):
    '''
    NB: I don't know if this is correct.
    @return: a CRC that is the FCS for the frame, as two hex bytes in
        little-endian order.
    '''
    crc = 0
    for i in xrange(len(packet)):
        c = ord(packet[i])
		#if (A PARITY BIT EXISTS): c = c & 127	#Mask off any parity bit
        q = (crc ^ c) & 15				#Do low-order 4 bits
        crc = (crc // 16) ^ (q * 4225)
        q = (crc ^ (c // 16)) & 15		#And high 4 bits
        crc = (crc // 16) ^ (q * 4225)
    return pack('<H', crc) #return as bytes in little endian order

class KZException(Exception):
        pass

# KillerZee Class
class KillerZee:

    MIN_PLEN_R1 = 9
    MAX_PLEN_R1 = 54
    MIN_PLEN_R2 = MIN_PLEN_R1
    MAX_PLEN_R2 = MAX_PLEN_R1
    MIN_PLEN_R3 = 11
    MAX_PLEN_R3 = 158
    MAX_PLEN = 0    # Set depending on RF profile selected
    MIN_PLEN = 0    # Set depending on RF profile selected

    regphy = {
            # CC: ( R1 frequency, R2 frequency, R3 frequency ),
            "US": (908419830, 908399994, 0),
            "CEPT": (868419678, 868399841, 0),
            "AU": (921399994, 919999939, 0),
            "HK": (919799988, 919599640, 0),
            "IN": (865199829, 864999878, 0),
            "MY": (868099915, 867899963, 0),
            "RU": (868.999695, 868799744, 0),
            }

    # According to http://z-wave.sigmadesigns.com/docs/Z-Wave_Frequency_Coverage.pdf,
    # Japan, Taiwan, and Koren all have ranges of frequencies.  I don't know if this means
    # they use multiple channels, or what their configuration might be.  Any help here
    # is welcome.

    # Canada, Chile and Mexico share the same frequency as the US
    regphy["CA"] = (regphy["US"][0], regphy["US"][1], regphy["US"][2])
    regphy["MX"] = (regphy["US"][0], regphy["US"][1], regphy["US"][2])
    regphy["CL"] = (regphy["US"][0], regphy["US"][1], regphy["US"][2])

    # New Zealand and Brazil share the same frequency as Australia
    regphy["BR"] = (regphy["AU"][0], regphy["AU"][1], regphy["AU"][2])
    regphy["NZ"] = (regphy["AU"][0], regphy["AU"][1], regphy["AU"][2])

    # The following countries are all CEPT-compliant
    regphy["AL"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["AD"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["AT"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["AZ"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["BY"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["BE"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["BA"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["BG"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["HR"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["CY"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["CZ"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["DK"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["EE"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["FI"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["FR"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["DE"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["GR"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["HU"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["IS"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["IE"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["IT"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["LV"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["LI"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["LT"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["LU"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["MT"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["MD"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["MC"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["NL"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["NO"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["PL"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["PT"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["RO"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["RU"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["SM"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["RS"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["SK"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["SI"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["ES"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["SE"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["CH"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["MK"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["TR"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["UA"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["GB"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["VA"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])

    # The following countries do not participate in CEPT but use the same frequency
    regphy["CN"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["SG"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["AE"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])
    regphy["ZA"] = (regphy["CEPT"][0], regphy["CEPT"][1], regphy["CEPT"][2])

    countrycode = None
    rfprofile = None

    # These are methods that are set when the profile type (R1, R2, R3) is set:
    pktpost = None
    decode = None
    inject = None

    _pktpost_packet = None
    calcfcs = None
    _kzd = KillerZeeDecode()



    def __init__(self, device=None, countrycode="US", rfprofile=RFPROFILE_R2):
        '''
        Instantiates the KillerZee class.

        @type device:   String
        @param device:  RfCat device identifier
        @return: None
        @rtype: None
        '''
        self.dev = RfCat(debug=False)
        self.set_regdomain(countrycode)
        self.set_rfprofile(rfprofile)



    def close(self):
        '''
        Closes the device out.
        @return: None
        @rtype: None
        '''


    def set_regdomain(self, countrycode="US"):
        '''
        Sets the radio regulatory domain to the correct frequency for the specified country code
        @type countrycode String
        @param countrycode: Sets the regulatory domain, default US
        @rtype: None
        '''
        try:
            if self.regphy[countrycode] != None:
                self.countrycode = countrycode
            else:
                raise KZException("Unsupported country code")
        except:
            raise KZException("Unsupported country code")


    def set_rfprofile(self, profile=RFPROFILE_R2):
        '''
        Sets the radio profile to the intended mode, one of R1, R2, or R3
        @type profile: Integer
        @param profile: Sets the profile, optional
        @rtype: None
        '''
        if self.countrycode == None:
            raise KZException("Must set country code.")
        if profile == RFPROFILE_R1:
            self._set_rfprofile_r1()
        elif profile == RFPROFILE_R2:
            self._set_rfprofile_r2()
        elif profile == RFPROFILE_R3:
            self._set_rfprofile_r3()
        else:
            raise KZExeception("Invalid profile definition specified")



    def _set_rfprofile_r1(self):
        # Check to ensure this profile is supported for the current regulatory domain
        try:
            if self.regphy[self.countrycode] == None:
                raise KZException("Invalid country code set; call set_regdomain() first")
        except:
            raise KZException("Invalid country code set; call set_regdomain() first")

        self.dev.setFreq(self.regphy[self.countrycode][RFPROFILE_R1])
        self.dev.setMdmModulation(MOD_2FSK)
        self.dev.setMdmSyncWord(0x55f0)
        self.dev.setMdmDeviatn(19042.969)
        self.dev.setMdmChanSpc(199951.172)
        self.dev.setMdmChanBW(101562.5)
        self.dev.setMdmDRate(19191.7)
        self.dev.makePktFLEN(54)
        self.dev.setEnableMdmManchester(True)
        self.dev.setMdmSyncMode(SYNCM_CARRIER_15_of_16)

        self.pktpost = self._pktpost_rfprofile_r1
        self.MIN_PLEN = self.MIN_PLEN_R1
        self.MAX_PLEN = self.MAX_PLEN_R1
        self.calcfcs = calcfcs_r1
        self.decode = self._kzd.decode_r1
        self.inject = self.inject_r1



    def _set_rfprofile_r2(self):
        # Check to ensure this profile is supported for the current regulatory domain
        try:
            if self.regphy[self.countrycode] == None:
                raise KZException("Invalid country code set; call set_regdomain() first")
        except:
            raise KZException("Invalid country code set; call set_regdomain() first")

        self.dev.setFreq(self.regphy[self.countrycode][RFPROFILE_R2])
        self.dev.setMdmModulation(MOD_2FSK)
        self.dev.setMdmSyncWord(0xaa0f)
        self.dev.setMdmDeviatn(20629.883)
        self.dev.setMdmChanSpc(199951.172)
        self.dev.setMdmChanBW(101562.5)
        self.dev.setMdmDRate(39970.4)
        self.dev.makePktFLEN(54)
        self.dev.setEnableMdmManchester(False)
        self.dev.setMdmSyncMode(SYNCM_CARRIER_15_of_16)

        self.pktpost = self._pktpost_rfprofile_r2
        self.MIN_PLEN = self.MIN_PLEN_R2
        self.MAX_PLEN = self.MAX_PLEN_R2
        self.calcfcs = calcfcs_r1
        self.decode = self._kzd.decode_r2
        self.inject = self.inject_r2


    def _set_rfprofile_r3(self):
        # No support for R3 yet
        raise KZException("No support for Z-Wave R3 profile yet.")

        self.pktpost = self._pktpost_rfprofile_r3
        self.MIN_PLEN = self.MIN_PLEN_R3
        self.MAX_PLEN = self.MAX_PLEN_R3
        self.calcfcs = calcfcs_r1


    def _pktpost_rfprofile_r1(self,packet):
        plen = ord(packet[7])
        if plen > len(packet):
            plen = len(packet)

        return packet[0:plen]
        return packet

    def _invert(self, data):
        datapost = ''
        for i in range(len(data)):
            datapost += chr(ord(data[i]) ^ 0xFF)
        return datapost

    def _pktpost_rfprofile_r2(self,packet):
        # All bits are inverted
        return self._invert(packet)


    def _pktpost_rfprofile_r3(self,packet):
        return packet


    def inject_r1(self, packet, count=1, delay=1):
        '''
        Injects the specified packet contents.
        @type packet: String
        @param packet: Packet contents to transmit, without FCS.
        @type count: Integer
        @param count: Transmits a specified number of frames, def=1
        @type delay: Float
        @param delay: Delay between each frame, def=1.0 seconds
        @rtype: None
        '''

        # To inject, we need to change the sync mode to SYNCM_CARRIER, and change
        # the length to the packet length + preamble + SFD
        # Save the previos sync mode and length settings to restore later
        PREAMBLE_R1="\x55" * 10
        SFD_R1 = "\xf0"
        EFD_R1 = "\x61" # The end frame delimeter is needed for R1, this works, but why?

        syncmode = self.dev.getMdmSyncMode()
        plen = self.dev.getPktLEN()[0] # returns a tuple (pktlen, pktctrl0)
        ppdu = PREAMBLE_R1 + SFD_R1 + packet + chr(self.calcfcs(packet)) + EFD_R1


        self.dev.setMdmSyncMode(SYNCM_CARRIER)
        self.dev.makePktFLEN(len(ppdu))
        while count != 0:
            self.dev.RFxmit(ppdu)
            count -= 1
            if count != 0:
                time.sleep(delay)

        self.dev.setMdmSyncMode(syncmode)
        self.dev.makePktFLEN(plen)


    def inject_r2(self, packet, count=1, delay=1, beam=True):
        '''
        Injects the specified packet contents.
        @type packet: String
        @param packet: Packet contents to transmit, without FCS.
        @type count: Integer
        @param count: Transmits a specified number of frames, def=1
        @type delay: Float
        @param delay: Delay between each frame, def=1.0 seconds
        @rtype: None
        '''

        # To inject, we need to change the sync mode to SYNCM_CARRIER, and change
        # the length to the packet length + preamble + SFD
        # Save the previos sync mode and length settings to restore later
        ### XXX TODO: If the packet is multicast, the PREAMBLE is 20 bytes min
        PREAMBLE_R2="\x55" * 10
        SFD_R2 = "\xf0"

        syncmode = self.dev.getMdmSyncMode()
        plen = self.dev.getPktLEN()[0] # returns a tuple (pktlen, pktctrl0)
        ppdu = PREAMBLE_R2 + SFD_R2 + packet + chr(self.calcfcs(packet))
        beamdata = PREAMBLE_R2 * 2 + SFD_R2 + "\x55\xff" # Wake everyone up

        # Invert bits prior to transmit
        ppdu = self._invert(ppdu)
        beamdata = self._invert(beamdata)

        self.dev.setMdmSyncMode(SYNCM_CARRIER)
        self.dev.makePktFLEN(len(ppdu))
        while count != 0:
            if beam:
                for i in range(300):
                    self.dev.RFxmit(beamdata)

            self.dev.RFxmit(ppdu)
            count -= 1
            if count != 0:
                time.sleep(delay)

        self.dev.setMdmSyncMode(syncmode)
        self.dev.makePktFLEN(plen)


    def pcap_next(self, timeout=1000):
        '''
        Returns a tuple with packet data as a string and a Bool for FCS check, else None.
        @type timeout: Integer
        @param timeout: Timeout to wait for packet reception in usec
        @rtype: List
        @return: Returns None is timeout expires and no packet received.  When a packet is received, a tuple is returned (String packet, Bool FCS_Correct)
        '''
        # The _pktpost functions will check to see if there is additional
        # data remaining that could be a packet (this is a limitation of
        # the Chipcon chip's ability to handle frame lengths).  See if there
        # is additional packet data to process before getting the next packet
        # from the RfCat interface.
        if self._pktpost_packet == None:
    
            # No previously buffered packet data remains to be processed, get the next
            # packet from RfCat
            packet = None
            try:
                packet = self.dev.RFrecv(timeout=timeout)[0] # Just the data, no timestamp
            except ChipconUsbTimeoutException:
                pass
            if packet == None:
                return None
    
            # Convert packet with Z-Wave profile-specific routine
            packet = self.pktpost(packet)
    
            # We have a buffer starting with a packet, but there could be other packets
            # in there as well, separated by SFD "\x55\xf0" bytes.
            # Split the buffer on the SFD value and process each piece as a packet.
            # Note: This will likely introduce packet loss as well, since "\x55\xf0" can happen
            # normally in a packet.  I don't have a better way to handle the RX data.
    
            pieces = packet.split("\x55\xf0")
            if len(pieces) > 1:
                self._pktpost_packet = pieces[1:]
            packet = pieces[0]
        else:
            packet = self._pktpost_packet[0]
            if len(self._pktpost_packet) > 1:
                self._pktpost_packet = self._pktpost_packet[1:]
            else:
                self._pktpost_packet = None

        if len(packet) < self.MIN_PLEN:
            return None

        # Get the packet length - we are trusting the reported length parameter here,
        # lacking a better way to identify the received frame length
        plen = ord(packet[7])
        if plen > len(packet):
            plen = len(packet) if len(packet) <= self.MAX_PLEN else self.MAX_PLEN

        hdr = (time.time(), plen, plen)
        return (hdr, packet[0:plen])
