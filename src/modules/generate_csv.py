# Generate CSV (Name,RGB,Hex)

def generate_csv (palette, filename):
    f = open(filename, 'w')

    # Header
    f.write('Color,RGB,Hex\n')

    # Colors
    for color in palette['colors']:
        f.write(color[3] + ',')
        f.write('{} {} {},'.format(*color[:3]))
        f.write('{:02X}{:02X}{:02X}\n'.format(*color[:3]))
        
    f.close()
