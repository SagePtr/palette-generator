# Generate JASC-PAL file

def generate_jasc (palette, filename):
    f = open(filename, 'w')

    # Header
    f.write('JASC-PAL\n');
    f.write('0100\n')
    f.write('{}\n'.format(len(palette['colors'])))

    # Colors
    for color in palette['colors']:
        f.write('%d %d %d\n' % tuple(color[:3]))
    
    f.close()
