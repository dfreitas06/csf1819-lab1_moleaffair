# uncompyle6 version 3.2.3
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 25 2016, 22:01:18) [MSC v.1900 32 bit (Intel)]
# Embedded file name: csfsteg/csfsteghide.py
# Compiled at: 2018-10-13 11:57:39
import sys, struct, numpy, PIL as pillow
from PIL import Image

def compose(array):
    bit_count = 0
    byte = ''
    data = ''
    for b in array:
        bit_count += 1
        byte += b

        if bit_count == 8:
            bit_count = 0
            data +=  chr(int(byte, 2))
            byte = ''
    return data

def decode_bit(b):
    return b[7] + b[6]

def get_size(array):
    size_array = array[:32]
    bit_count = 0
    byte = ''
    p_size = ''
    for b in size_array:
        bit_count += 1
        byte += b

        if bit_count == 8:
            bit_count = 0
            p_size += chr(int(byte, 2))
            byte = ''

    return struct.unpack('i', p_size)[0]


def debed(imgFile, password, newname):
    img = Image.open(imgFile)
    width, height = img.size 
    conv = img.convert('RGBA').getdata()
    print '[*] Input image size: %dx%d pixels.' % (width, height)
    
    v = []
    displacement = 0
    for h in range(height):
        for w in range(width):
            if displacement < password:
                displacement = displacement + 1
                continue

            r, g, b, a = conv.getpixel((w, h))
            r = '{0:08b}'.format(r)
            g = '{0:08b}'.format(g)
            b = '{0:08b}'.format(b)

            r_dec = decode_bit(r)
            g_dec = decode_bit(g)
            b_dec = decode_bit(b)
                
            v.append(r_dec[0])
            v.append(r_dec[1])
            v.append(g_dec[0])
            v.append(g_dec[1])
            v.append(b_dec[0])
            v.append(b_dec[1])
            
    size = get_size(v)
    size_b = size * 8
    data = compose(v[32:size_b + 32])

    f = open(newname, "w")
    f.write(data)
    f.close()

def usage(progName):
    print('Ciber Securanca Forense - Instituto Superior Tecnico / Universidade Lisboa')
    print('LSB steganography tool: hide files within least significant bits of images.\n')
    print('')
    print('Usage:')
    print('  %s <img_file> <info_filename> [password]', progName)
    print('')
    print('  The password is optional and must be a number.')
    sys.exit()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage(sys.argv[0])
    password = int(sys.argv[3]) % 13 if len(sys.argv) > 3 else 0
    debed(sys.argv[1], password, sys.argv[2])
# okay decompiling compress.pyc
