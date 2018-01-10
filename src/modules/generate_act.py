# Generate Adobe Color Table

from struct import pack

def generate_act (palette, filename):
    f = open(filename, 'wb')
    colors = palette['colors']

    # Colors
    for color in colors:
        f.write(pack('3B', *color[:3]))

    # Rest of colors
    for color in range(len(colors), 256):
        f.write(b'\x00\x00\x00')

    # Footer (if not exactly 256 colors)
    if len(colors) < 256:
        f.write(pack('4B', 0, len(colors), 255, 255))
        
        
    f.close()
