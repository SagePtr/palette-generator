# Generate GIMP Palette

def generate_gpl (palette, filename):
    f = open(filename, 'w')
    
    f.write('GIMP Palette\n');
    f.write('Name: ' + palette['name'] + '\n')
    f.write('Columns: ' + str(palette['columns']) + '\n')
    if len(palette['comments']) > 0:
        f.write('#\n')
        for line in palette['comments']:
            f.write('# ' + line + '\n')
    f.write('#\n')
    for color in palette['colors']:
        f.write(str(color[0]).rjust(3))
        f.write(str(color[1]).rjust(4))
        f.write(str(color[2]).rjust(4))
        f.write('\t' + color[3] + '\n')
        
    f.close()
