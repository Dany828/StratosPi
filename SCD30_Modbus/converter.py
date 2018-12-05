from ctypes import *

class Converter:

    @staticmethod
    def floatToBytes(bigendian, value):
        # initialise return data
        data = [0,0,0,0]

        # pointer to float value
        ptr = pointer(c_float(value))
        
        # cast to int pointer
        ip = cast(ptr, POINTER(c_int))
        
        # retrieve integer value
        intvalue = ip.contents.value

        if bigendian:
            data[0] = (intvalue & 0xFF000000) >> 24
            data[1] = (intvalue & 0x00FF0000) >> 16
            data[2] = (intvalue & 0x0000FF00) >> 8
            data[3] = (intvalue & 0x000000FF)
        else:
            data[3] = (intvalue & 0xFF000000) >> 24
            data[2] = (intvalue & 0x00FF0000) >> 16
            data[1] = (intvalue & 0x0000FF00) >> 8
            data[0] = (intvalue & 0x000000FF)

        return data


    @staticmethod
    def bytesToFloat(bigendian, datain):

        if bigendian:
            intvalue = datain[0] << 24
            intvalue += datain[1] << 16
            intvalue += datain[2] << 8
            intvalue += datain[3]
        else:
            intvalue = datain[0]
            intvalue += datain[1] << 8
            intvalue += datain[2] << 16
            intvalue += datain[3] << 24
        
        # pointer to integer value
        ptr = pointer(c_int(intvalue))
        
        # cast to float pointer
        fp = cast(ptr, POINTER(c_float))
        
        # return float value
        return fp.contents.value




