# Generate Adobe Swatches for Exchange
# Format spec: http://www.selapa.net/swatches/colors/fileformats.php#adobe_ase
# Another format explaination: http://carl.camera/?id=109

from struct import pack

def asef_chunk (type, data):
    # Chunk type (long)
    result = pack('>L', type)
    # Chunk length in bytes
    result += pack('>H', len(data))
    # Chunk content
    result += data

    return result

def asef_color (color):
    # Color name
    result = asef_text(color[3])
    # Colorspace
    result += b'RGB '
    # Components as float
    result += pack('>3f', *map(lambda x: x/255.0, color[:3]))
    # Color type (0=global,1=spot,2=normal)
    result += b'\x00\x00'
    
    return result
    
def asef_text (str):
    # Null-terminate string
    ustr = str + '\x00'
    # Lenght of string in chars (including null-terminator)
    ulen = len(ustr)
    # Convert this string to UTF-16 big-endian
    ustr = ustr.encode('utf-16be')
    
    return pack('>H', ulen) + ustr

def generate_ase (palette, filename):
    f = open(filename, 'wb')

    # Header
    f.write(b'ASEF\x00\x01\x00\x00')
    # Number of blocks (colors + 2 for group header/footer)
    f.write(pack('>L', len(palette['colors']) + 2))
    # Group header
    f.write(asef_chunk(0xC0010000, asef_text(palette['name'])))
    # Colors
    for color in palette['colors']:
        f.write(asef_chunk(0x00010000, asef_color(color)))
    # Group footer
    f.write(asef_chunk(0xC0020000, b''))
        
    f.close()
