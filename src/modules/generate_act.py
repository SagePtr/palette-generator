# Generate Adobe Color Table

from struct import pack

def generate_act (palette, filename):
    f = open(filename, 'wb')
    colors = palette['colors']
    
    for color in colors:
        f.write(pack('3B', *color[:3]))
    for color in xrange(len(colors), 256):
        f.write('\x00\x00\x00')

    if len(colors) < 256:
        f.write(pack('4B', 0, len(colors), 255, 255))
        
        
    f.close()
