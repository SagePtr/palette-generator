# Generate GIMP Palette

def generate_gpl (palette, filename):
    f = open(filename, 'w')
    
    # Palette header
    f.write('GIMP Palette\n');
    f.write('Name: {}\n'.format(palette['name']))
    f.write('Columns: {}\n'.format(palette['columns']))
    
    # Comments (at least one blank comment)
    if len(palette['comments']) > 0:
        f.write('#\n')
        for line in palette['comments']:
            f.write('# {}\n'.format(line))
    f.write('#\n')
    
    # Colors
    for color in palette['colors']:
        f.write('{:3}{:4}{:4}\t{}\n'.format(*color))
        
    f.close()
