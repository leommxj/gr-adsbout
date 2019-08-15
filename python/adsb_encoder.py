import numpy
import math
import sys

class Encoder:
    """
    Hamming and Manchester Encoding example

    Author: Joel Addison
    Date: March 2013

    Functions to do (7,4) hamming encoding and decoding, including error detection
    and correction.
    Manchester encoding and decoding is also included, and by default will use
    least bit ordering for the byte that is to be included in the array.
    """

    def extract_bit(self, byte, pos):
        """
        Extract a bit from a given byte using MS ordering.
        ie. B7 B6 B5 B4 B3 B2 B1 B0
        """
        return (byte >> pos) & 0x01

    def manchester_encode(self, byte):
        """
        Encode a byte using Manchester encoding. Returns an array of bits.
        Adds two start bits (1, 1) and one stop bit (0) to the array.
        """
        # Add start bits (encoded 1, 1)
        # manchester_encoded = [0, 1, 0, 1]
        manchester_encoded = []

        # Encode byte
        for i in range(7, -1, -1):
            if self.extract_bit(byte, i):
                manchester_encoded.append(0)
                manchester_encoded.append(1)
            else:
                manchester_encoded.append(1)
                manchester_encoded.append(0)

        # Add stop bit (encoded 0)
        # manchester_encoded.append(1)
        # manchester_encoded.append(0)

        return manchester_encoded


class PPM:
    """The PPM class contains functions about PPM manipulation
    """

    def frame_1090es_ppm_modulate_normal(self, in_bytes):
        """
        Args:
            in_bytes: The bits you would converted to PPM
        Returns:
            The bytearray of the PPM data
        """
        ppm = [ ]
        encoder = Encoder()

        for i in range(48):    # pause
            ppm.append( 0 )

        ppm.append( 0xA1 )   # preamble
        ppm.append( 0x40 )
        
        for i in range(len(in_bytes)):
            word16 = numpy.packbits(encoder.manchester_encode(~in_bytes[i]))
            ppm.append(word16[0])
            ppm.append(word16[1])


        for i in range(100):    # pause
            ppm.append( 0 )
        
        return bytearray(ppm)

 
    def frame_1090es_ppm_modulate(self, even, odd):
        """
        Args:
            even and odd: The bits you would converted to PPM
        Returns:
            The bytearray of the PPM data
        """
        ppm = [ ]
        encoder = Encoder()

        for i in range(48):    # pause
            ppm.append( 0 )

        ppm.append( 0xA1 )   # preamble
        ppm.append( 0x40 )
        
        for i in range(len(even)):
            word16 = numpy.packbits(encoder.manchester_encode(~even[i]))
            ppm.append(word16[0])
            ppm.append(word16[1])


        for i in range(100):    # pause
            ppm.append( 0 )

        ppm.append( 0xA1 )   # preamble
        ppm.append( 0x40 )

        for i in range(len(odd)):
            word16 = numpy.packbits(encoder.manchester_encode(~odd[i]))
            ppm.append(word16[0])
            ppm.append(word16[1])

        for i in range(48):    # pause
            ppm.append( 0 )

        #print '[{}]'.format(', '.join(hex(x) for x in ppm))
        
        return bytearray(ppm)
        
    def addGap(self, gap):
        """
        This function will add dead air as a gap between messages
        Args:
            gap: The number of microseconds to have as a gap
        Returns:
            The bytearray of the PPM data
        """
        ppm = [ ]
        for i in range(gap):    # pause
            ppm.append( 0 )
        return bytearray(ppm)

class ModeSLocation:
    """This class does ModeS/ADSB Location calulations"""

    def encode_alt_modes(self, alt, bit13):
        # need to better understand as the >50175 feet not working
        # TODO >50175 feet
        mbit = False
        qbit = True
        # For altitudes -1000<=X<=50175 feet, set bit 8 AKA the Q bit to true which means 25 feet resoulution
        # For >50175 set the qbit to False and use 100 feet resoultion
        if alt > 50175:
            qbit = False
            encalt = int((int(alt) + 1000) / 100)
        else:
            qbit = True
            encalt = int((int(alt) + 1000) / 25)

        if bit13 is True:
            tmp1 = (encalt & 0xfe0) << 2
            tmp2 = (encalt & 0x010) << 1

        else:
            tmp1 = (encalt & 0xff8) << 1
            tmp2 = 0

        return (encalt & 0x0F) | tmp1 | tmp2 | (mbit << 6) | (qbit << 4)

    latz = 15

    def nz(self, ctype):
	    """
	    Number of geographic latitude zones between equator and a pole. It is set to NZ = 15 for Mode-S CPR encoding
	    https://adsb-decode-guide.readthedocs.io/en/latest/content/cpr.html
	    """
	    return 4 * self.latz - ctype

    def dlat(self, ctype, surface):
	    if surface == 1:
		    tmp = 90.0
	    else:
		    tmp = 360.0

	    nzcalc = self.nz(ctype)
	    if nzcalc == 0:
		    return tmp
	    else:
		    return tmp / nzcalc

    def nl(self, declat_in):
	    if abs(declat_in) >= 87.0:
		    return 1.0
	    return math.floor( (2.0*math.pi) * math.acos(1.0- (1.0-math.cos(math.pi/(2.0*self.latz))) / math.cos( (math.pi/180.0)*abs(declat_in) )**2 )**-1)

    def dlon(self, declat_in, ctype, surface):
	    if surface:
		    tmp = 90.0
	    else:
		    tmp = 360.0
	    nlcalc = max(self.nl(declat_in)-ctype, 1)
	    return tmp / nlcalc

    #encode CPR position
    # https://adsb-decode-guide.readthedocs.io/en/latest/content/cpr.html
    # compact position reporting
    def cpr_encode(self, lat, lon, ctype, surface):
        if surface is True:
            scalar = 2.**19
        else:
            scalar = 2.**17

        #encode using 360 constant for segment size.
        dlati = self.dlat(ctype, False)
        yz = math.floor(scalar * ((lat % dlati)/dlati) + 0.5)
        rlat = dlati * ((yz / scalar) + math.floor(lat / dlati))
        
        #encode using 360 constant for segment size.
        dloni = self.dlon(lat, ctype, False)
        xz = math.floor(scalar * ((lon % dloni)/dloni) + 0.5)
        
        yz = int(yz) & (2**17-1)
        xz = int(xz) & (2**17-1)
        
        return (yz, xz) #lat, lon

class ModeS:
    """This class handles the ModeS ADSB manipulation
    """
    def df17_velocity_encode(self, icao, st):
        """
            This function will generate an adsb df17 typecode 19 velocity message from given arguments
        """
        format = 17
        ca = 5
        tc = 19 
        ident_bytes = []
        ident_bytes.append((format<<3) | ca)
        ident_bytes.append((icao>>16) & 0xff)
        ident_bytes.append((icao>> 8) & 0xff)
        ident_bytes.append((icao    ) & 0xff)
        ident_bytes.append((tc<<3) | ec)
        pass
        # TODO

    def df17_ident_encode(self, ec, icao, callsign):
        """
            This function will generate an adsb df17 typecode 4 identification message from given arguments
        """
        alphabet = "#ABCDEFGHIJKLMNOPQRSTUVWXYZ#####_###############0123456789######"

        format = 17
        ca = 5
        tc = 4
        ident_bytes = []
        ident_bytes.append((format<<3) | ca)
        ident_bytes.append((icao>>16) & 0xff)
        ident_bytes.append((icao>> 8) & 0xff)
        ident_bytes.append((icao    ) & 0xff)
        ident_bytes.append((tc<<3) | ec)
        callsign_bytes = []
        for c in callsign:
            callsign_bytes.append(alphabet.index(c))
        while len(callsign_bytes)<8:
            callsign_bytes.append(32)
        
        ident_bytes.append(((callsign_bytes[0]<<2)|(callsign_bytes[1]>>4))&0xff)
        ident_bytes.append(((callsign_bytes[1]<<4)|(callsign_bytes[2]>>2))&0xff)
        ident_bytes.append(((callsign_bytes[2]<<6)|(callsign_bytes[3]>>0))&0xff)
        ident_bytes.append(((callsign_bytes[4]<<2)|(callsign_bytes[5]>>4))&0xff)
        ident_bytes.append(((callsign_bytes[5]<<4)|(callsign_bytes[6]>>2))&0xff)
        ident_bytes.append(((callsign_bytes[6]<<6)|(callsign_bytes[7]>>0))&0xff)
        ident_str = "{0:02x}{1:02x}{2:02x}{3:02x}{4:02x}{5:02x}{6:02x}{7:02x}{8:02x}{9:02x}{10:02x}".format(*ident_bytes[0:11])
        ident_crc = self.bin2int(self.modes_crc(ident_str+"000000", encode=True))
        ident_bytes.append((ident_crc>16) & 0xff)
        ident_bytes.append((ident_crc> 8) & 0xff)
        ident_bytes.append((ident_crc   ) & 0xff)    
        
        return ident_bytes


    
    def df17_pos_rep_encode(self, ca, icao, tc, ss, nicsb, alt, time, lat, lon, surface):
        """
        This will take the parameters for an ADSB type 17 message and reutrn the even and odd bytes
        """

        format = 17 #The format type of an ADSB message

        location = ModeSLocation()
        enc_alt =	location.encode_alt_modes(alt, surface)
        #print "Alt(%r): %X " % (surface, enc_alt)
        
        #encode that position
        (evenenclat, evenenclon) = location.cpr_encode(lat, lon, False, surface)
        (oddenclat, oddenclon)   = location.cpr_encode(lat, lon, True, surface)

        #print "Even Lat/Lon: %X/%X " % (evenenclat, evenenclon)
        #print "Odd  Lat/Lon: %X/%X " % (oddenclat, oddenclon)

        ff = 0
        df17_even_bytes = []
        df17_even_bytes.append((format<<3) | ca)
        df17_even_bytes.append((icao>>16) & 0xff)
        df17_even_bytes.append((icao>> 8) & 0xff)
        df17_even_bytes.append((icao    ) & 0xff)
        # data
        df17_even_bytes.append((tc<<3) | (ss<<1) | nicsb)
        df17_even_bytes.append((enc_alt>>4) & 0xff)
        df17_even_bytes.append((enc_alt & 0xf) << 4 | (time<<3) | (ff<<2) | (evenenclat>>15))
        df17_even_bytes.append((evenenclat>>7) & 0xff)    
        df17_even_bytes.append(((evenenclat & 0x7f) << 1) | (evenenclon>>16))  
        df17_even_bytes.append((evenenclon>>8) & 0xff)   
        df17_even_bytes.append((evenenclon   ) & 0xff)

        df17_str = "{0:02x}{1:02x}{2:02x}{3:02x}{4:02x}{5:02x}{6:02x}{7:02x}{8:02x}{9:02x}{10:02x}".format(*df17_even_bytes[0:11])
        #print df17_str , "%X" % bin2int(crc(df17_str+"000000", encode=True)) , "%X" % get_parity(hex2bin(df17_str+"000000"), extended=True)
        df17_crc = self.bin2int(self.modes_crc(df17_str+"000000", encode=True))

        df17_even_bytes.append((df17_crc>>16) & 0xff)
        df17_even_bytes.append((df17_crc>> 8) & 0xff)
        df17_even_bytes.append((df17_crc    ) & 0xff)
     
        ff = 1
        df17_odd_bytes = []
        df17_odd_bytes.append((format<<3) | ca)
        df17_odd_bytes.append((icao>>16) & 0xff)
        df17_odd_bytes.append((icao>> 8) & 0xff)
        df17_odd_bytes.append((icao    ) & 0xff)
        # data
        df17_odd_bytes.append((tc<<3) | (ss<<1) | nicsb)
        df17_odd_bytes.append((enc_alt>>4) & 0xff)
        df17_odd_bytes.append((enc_alt & 0xf) << 4 | (time<<3) | (ff<<2) | (oddenclat>>15))
        df17_odd_bytes.append((oddenclat>>7) & 0xff)    
        df17_odd_bytes.append(((oddenclat & 0x7f) << 1) | (oddenclon>>16))  
        df17_odd_bytes.append((oddenclon>>8) & 0xff)   
        df17_odd_bytes.append((oddenclon   ) & 0xff)

        df17_str = "{0:02x}{1:02x}{2:02x}{3:02x}{4:02x}{5:02x}{6:02x}{7:02x}{8:02x}{9:02x}{10:02x}".format(*df17_odd_bytes[0:11])
        df17_crc = self.bin2int(self.modes_crc(df17_str+"000000", encode=True))

        df17_odd_bytes.append((df17_crc>>16) & 0xff)
        df17_odd_bytes.append((df17_crc>> 8) & 0xff)
        df17_odd_bytes.append((df17_crc    ) & 0xff)    
        
        return (df17_even_bytes, df17_odd_bytes)
        
    def modes_crc(self, msg, encode=False):
        """Mode-S Cyclic Redundancy Check
        Detect if bit error occurs in the Mode-S message
        Args:
            msg (string): 28 bytes hexadecimal message string
            encode (bool): True to encode the date only and return the checksum
        Returns:
            string: message checksum, or partity bits (encoder)
        """

        GENERATOR = "1111111111111010000001001" # Currently don't know what is magic about this number

        msgbin = list(self.hex2bin(msg))

        if encode:
            msgbin[-24:] = ['0'] * 24

        # loop all bits, except last 24 piraty bits
        for i in range(len(msgbin)-24):
            # if 1, perform modulo 2 multiplication,
            if msgbin[i] == '1':
                for j in range(len(GENERATOR)):
                    # modulo 2 multiplication = XOR
                    msgbin[i+j] = str((int(msgbin[i+j]) ^ int(GENERATOR[j])))

        # last 24 bits
        reminder = ''.join(msgbin[-24:])
        return reminder
    
            
        
    def hex2bin(self, hexstr):
        """Convert a hexdecimal string to binary string, with zero fillings. """
        scale = 16
        num_of_bits = len(hexstr) * math.log(scale, 2)
        binstr = bin(int(hexstr, scale))[2:].zfill(int(num_of_bits))
        return binstr

    def bin2int(self, binstr):
        """Convert a binary string to integer. """
        return int(binstr, 2)


class HackRF:
    """The HackRF class has functions from converting data into a format into which the hackrf can process
    """
    
    def __init__(self):
        pass

    def hackrf_raw_IQ_format(self, ppm):
        """
        Args:
            ppm: this is some data in ppm (pulse position modulation) which you want to convert into raw IQ format
            
        Returns:
            bytearray: containing the IQ data
        """
        signal = []
        bits = numpy.unpackbits(numpy.asarray(ppm, dtype=numpy.uint8))
        for bit in bits:
            if bit == 1:
                I = 127
                Q = 127
            else:
                I = 0
                Q = 0
            signal.append(I)
            signal.append(Q)

        return bytearray(signal)


def gen_position(arguments):
    samples = bytearray()
    modes = ModeS()
    (df17_even, df17_odd) = modes.df17_pos_rep_encode(arguments.capability, arguments.icao, arguments.typecode, arguments.surveillancestatus, arguments.nicsupplementb, arguments.altitude, arguments.time, arguments.latitude, arguments.longitude, arguments.surface)

    ppm = PPM()
    df17_array = ppm.frame_1090es_ppm_modulate(df17_even, df17_odd)

    hackrf = HackRF()
    samples_array = hackrf.hackrf_raw_IQ_format(df17_array)
    samples = samples + samples_array
    #gap_array = ppm.addGap(arguments.intermessagegap)
    #samples_array = hackrf.hackrf_raw_IQ_format(gap_array)
    #samples = samples + samples_array
    sys.stderr.write("len:{:d}\n".format(len(samples)))
    return samples
    #return samples.rjust(0x40000,'\x00')

def gen_ident(arguments):
    samples = bytearray()
    modes = ModeS()
    ppm = PPM()
    hackrf = HackRF()

    ident_bytes = modes.df17_ident_encode(arguments.ec, arguments.icao, arguments.callsign)
    ident_array = ppm.frame_1090es_ppm_modulate_normal(ident_bytes)
    samples_array = hackrf.hackrf_raw_IQ_format(ident_array)
    samples = samples+samples_array
    #gap_array = ppm.addGap(arguments.intermessagegap)
    #samples_array = hackrf.hackrf_raw_IQ_format(gap_array)
    #samples = samples+samples_array
    sys.stderr.write("len:{}\n".format(len(samples)))
    return samples
    #return samples.rjust(0x40000,'\x00')

def gen_velocity(arguments):
    pass
    

if __name__ == '__main__':
    print("o")
