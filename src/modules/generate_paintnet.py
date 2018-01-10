# Generate Paint.net Palette

def generate_paintnet (palette, filename):
    f = open(filename, 'w')

    # Header
    f.write('; paint.net Palette File\n');
    f.write('; Name: {}\n'.format(palette['name']))

    # Comments
    for line in palette['comments']:
        f.write('; {}\n'.format(line))

    # Colors
    for color in palette['colors']:
        f.write('FF{:02X}{:02X}{:02X}\n'.format(*color))
        
    f.close()
