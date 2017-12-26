# Generate JASC-PAL file

def generate_jasc (palette, filename):
    f = open(filename, 'w')
    
    f.write('JASC-PAL\n');
    f.write('0100\n')
    f.write('%d\n' % len(palette['colors']))
    for color in palette['colors']:
        f.write('%d %d %d\n' % tuple(color[:3]))
    
    f.close()
