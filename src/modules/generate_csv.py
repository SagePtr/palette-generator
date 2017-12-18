# Generate CSV (Name,RGB,Hex)

def generate_csv (palette, filename):
    f = open(filename, 'w')

    f.write('Color,RGB,Hex\n')
    
    for color in palette['colors']:
        f.write(color[3] + ',')
        f.write('%d %d %d,' % tuple(color[:3]))
        f.write('%02X%02X%02X\n' % tuple(color[:3]))
        
    f.close()
