# Generate Paint.net Palette

from generate_utils import colorhex

def generate_paintnet (palette, filename):
    f = open(filename, 'w')
    
    f.write('; paint.net Palette File\n');
    f.write('; Name: ' + palette['name'] + '\n')
    
    for line in palette['comments']:
        f.write('; ' + line + '\n')

    for color in palette['colors']:
        f.write('FF' + colorhex(color).upper() + '\n')
        
    f.close()
