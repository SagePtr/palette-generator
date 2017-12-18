import os
import glob
import re
import zlib
from modules.generate_gpl import *
from modules.generate_paintnet import *
from modules.generate_csv import *
from modules.generate_act import *
from modules.generate_ase import *
from modules.generate_png import *
from modules.generate_unity import *

rootdir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

def process_palette (filename):
    palette = {}
    palette['id'] = os.path.splitext(os.path.basename(filename))[0]
    palette['name'] = palette['id']
    palette['colors'] = []
    palette['columns'] = 8
    palette['comments'] = []
    print ('Processing %s...' % palette['id'])
    # Parse Gimp palette file
    f = open(filename, 'r')
    lines = f.read().splitlines()
    f.close()
    if lines[0] != 'GIMP Palette':
        raise Exception('%s must be GIMP palette' % filename)
    for i in xrange(1, len(lines)):
        line = lines[i]
        m = re.match(r'^Name: ([^#]+)', line)
        if m:
            palette['name'] = m.group(1)
        m = re.match(r'Columns: (\d+)', line)
        if m:
            palette['columns'] = int(m.group(1))
        m = re.match(r'#(.+)', line)
        if m:
            palette['comments'].append(m.group(1).strip())
        m = re.match(r'\s*(\d{1,3})\s+(\d{1,3})\s+(\d{1,3})\s+([^#]+)', line)
        if m:
            color = []
            for t in xrange(1,4):
                component = int(m.group(t))
                if component < 0 or component > 255:
                    raise Exception('Invalid color: %s' % m.group(0))
                color.append(component)
            colorname = m.group(4).strip()
            if not colorname or colorname == 'Untitled':
                colorname = '#%02x%02x%02x' % tuple(color)
            color.append(colorname)
            palette['colors'].append(color)
    print ('Parsed %s (%s, %d colors)' % (filename, palette['name'], len(palette['colors'])))
    # Create directory for output
    outdir = rootdir + '/build/' + palette['id']
    try:
        os.makedirs(outdir)
    except OSError:
        pass
    # Generate gpl
    outfile = outdir + '/' + palette['id'] + '.gpl'
    generate_gpl(palette, outfile)
    print ('Generated ' + outfile)
    # Generate PNG
    outfile = outdir + '/' + palette['id'] + '.png'
    generate_png(palette, outfile)
    print ('Generated ' + outfile)
    # Generate Paint.net
    outfile = outdir + '/' + palette['id'] + '.txt'
    generate_paintnet(palette, outfile)
    print ('Generated ' + outfile)
    # Generate CSV
    outfile = outdir + '/' + palette['id'] + '.csv'
    generate_csv(palette, outfile)
    print ('Generated ' + outfile)
    # Generate Adobe color table
    outfile = outdir + '/' + palette['id'] + '.act'
    generate_act(palette, outfile)
    print ('Generated ' + outfile)
    # Generate Adobe Swatches for Exchange
    outfile = outdir + '/' + palette['id'] + '.ase'
    generate_ase(palette, outfile)
    print ('Generated ' + outfile)
    # Generate Unity assets
    outfile = outdir + '/' + palette['id'] + '.colors'
    generate_unity(palette, outfile)
    print ('Generated ' + outfile)
    
    #print palette


# Scan palettes directory and build each palette
print (rootdir + '/palettes/*.gpl')
palettes = glob.glob(rootdir + '/palettes/*.gpl')
for palette in palettes:
    process_palette(palette)
