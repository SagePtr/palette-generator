# Generate PNG
# https://www.w3.org/TR/2003/REC-PNG-20031110/

import zlib
import math
from struct import pack

def png_chunk (type, data):
    # Chunk size
    result = pack('>L', len(data))
    # Chunk type
    result += type
    # Chunk content
    result += data
    # Chunk CRC
    result += pack('>l', zlib.crc32(type + data))
    return result

def generate_png (palette, filename, item_size = 32):
    f = open(filename, 'wb')
    columns = palette['columns']
    colors = palette['colors']
    numcolors = len(colors)
    width_b = min(columns, numcolors)
    width_px = width_b * item_size
    height_b = int(math.ceil(numcolors / float(columns)))
    height_px = height_b * item_size
    # Magic
    f.write('\x89PNG\x0D\x0A\x1A\x0A')
    # IHDR
    ihdr = pack('>2L5B', width_px, height_px, 8, 3, 0, 0, 0)
    f.write(png_chunk('IHDR', ihdr))
    # tEXt
    #f.write(png_chunk('tEXt', 'Title\x00' + palette['name']))
    # PLTE
    plte = ''.join(map(lambda x: pack('3B', *x[:3]), colors))
    f.write(png_chunk('PLTE', plte))
    # IDAT
    idat = ''
    index = 0
    # Very hacky filtering
    # For first scanline of each color row, we use filter SUB (0x01)
    #  First pixel of scanline is color index, because it has no prev pixel
    #   then, we fill with blank columns (0x00) as they don't differ
    #  Each first pixel of each color is 0x01
    #   then, we fill with blank columns (0x00) as they don't differ
    # Later scanlines are blank. Filter UP is used (0x02) + zero pixels till end
    # TODO: probably reduce BPP for palettes <= 16, but no much size difference
    for row in xrange(0, height_b):
        idat += '\x01' #filter (prev)
        # first color of column
        idat += pack('B', index)
        index += 1
        # extra pixels of first color
        idat += '\x00' * (item_size-1)
        # extra colors in column
        for col in xrange(1, width_b):
            if index >= numcolors:
                # if we ran out of palette - fill with color 0 (usually black)
                idat += pack('B', (257-index) % 256)
                idat += '\x00' * ((width_b - col) * item_size - 1)
                break
            idat += '\x01' if index < numcolors else '\x00'
            idat += '\x00' * (item_size-1)
            index += 1
        # Fill extra scanlines width UP filter
        idat += ('\x02' + ('\x00' * width_px)) * (item_size-1)
    f.write(png_chunk('IDAT', zlib.compress(idat, 9)))
    # IEND
    f.write(png_chunk('IEND', ''))
        
    f.close()
