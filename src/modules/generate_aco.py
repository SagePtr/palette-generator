# Generate Adobe Color Swatches (ACO)
# Format spec: http://www.selapa.net/swatches/colors/fileformats.php#adobe_aco
# http://www.adobe.com/devnet-apps/photoshop/fileformatashtml/#50577411_pgfId-1055819

from struct import pack

def aco_color (color):
    result = '\x00\x00' #RGB color space
    result += ''.join(map(lambda x: chr(x)*2, color[:3]))
    result += '\x00\x00'
    return result

#Same as asef_text, by length is four bytes    
def aco_text (str):
    # Null-terminate string
    ustr = str + '\x00'
    # Lenght of string in chars (including null-terminator)
    ulen = len(ustr)
    # Convert this string to UTF-16 big-endian
    ustr = ustr.encode('utf-16be')

    return pack('>L', ulen) + ustr

def generate_aco (palette, filename):
    f = open(filename, 'wb')

    # Version 1
    f.write('\x00\x01')
    f.write(pack('>H', len(palette['colors'])))
    # Colors (without text)
    for color in palette['colors']:
        f.write(aco_color(color))
    # Version 2
    f.write('\x00\x02')
    f.write(pack('>H', len(palette['colors'])))
    # Colors (with text)
    for color in palette['colors']:
        f.write(aco_color(color))
        f.write(aco_text(color[3]))
        
    f.close()
