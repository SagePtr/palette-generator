import os
import glob
import re
import zlib
from modules.generate_gpl import generate_gpl
from modules.generate_jasc import generate_jasc
from modules.generate_paintnet import generate_paintnet
from modules.generate_csv import generate_csv
from modules.generate_act import generate_act
from modules.generate_aco import generate_aco
from modules.generate_ase import generate_ase
from modules.generate_png import generate_png
from modules.generate_unity import generate_unity

ROOTDIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
INDIR = os.path.join(ROOTDIR, 'palettes')
OUTDIR = os.path.join(ROOTDIR, 'build')

def process_palette (filename):
    palette = {}
    palette['id'] = os.path.splitext(os.path.basename(filename))[0]
    palette['name'] = palette['id']
    palette['colors'] = []
    palette['columns'] = 8
    palette['comments'] = []
    print ('Processing {}...'.format(filename))
    
    # Parse Gimp palette file
    f = open(os.path.join(INDIR, filename), 'r')
    lines = f.read().splitlines()
    f.close()
    if lines[0] != 'GIMP Palette':
        raise Exception('{} must be GIMP palette'.format(filename))
    for i in range(1, len(lines)):
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
        m = re.match(r'\s*(\d{1,3})\s+(\d{1,3})\s+(\d{1,3})\s+(.*)', line)
        if m:
            color = []
            for t in range(1,4):
                component = int(m.group(t))
                if component < 0 or component > 255:
                    raise Exception('Invalid color: {}'.format(m.group(0)))
                color.append(component)
            colorname = m.group(4).strip()
            if not colorname or colorname == 'Untitled':
                colorname = '#{:02X}{:02X}{:02X}'.format(*color)
            color.append(colorname)
            palette['colors'].append(color)
    print ('Parsed {} ({}, {} colors)'.format(
        filename, palette['name'], len(palette['colors'])))
    
    # Create directory for output
    outdir = os.path.join(OUTDIR, os.path.dirname(filename), palette['id'])
    print ('IN: {}, OUT: {}'.format(filename, outdir))
    try:
        os.makedirs(outdir)
    except OSError:
        pass
    
    # Generate gpl
    outfile = os.path.join(outdir, palette['id'] + '.gpl')
    generate_gpl(palette, outfile)
    print ('Generated ' + outfile)
    
    # Generate PNG
    outfile = os.path.join(outdir, palette['id'] + '.png')
    generate_png(palette, outfile)
    print ('Generated ' + outfile)
    
    # Generate JASC-PAL
    outfile = os.path.join(outdir, palette['id'] + '.pal')
    generate_jasc(palette, outfile)
    print ('Generated ' + outfile)
    
    # Generate Paint.net
    outfile = os.path.join(outdir, palette['id'] + '.txt')
    generate_paintnet(palette, outfile)
    print ('Generated ' + outfile)
    
    # Generate CSV
    outfile = os.path.join(outdir, palette['id'] + '.csv')
    generate_csv(palette, outfile)
    print ('Generated ' + outfile)
    
    # Generate Adobe Color Table
    outfile = os.path.join(outdir, palette['id'] + '.act')
    generate_act(palette, outfile)
    print ('Generated ' + outfile)
    
    # Generate Adobe Color Swatches
    outfile = os.path.join(outdir, palette['id'] + '.aco')
    generate_aco(palette, outfile)
    print ('Generated ' + outfile)
    
    # Generate Adobe Swatches for Exchange
    outfile = os.path.join(outdir, palette['id'] + '.ase')
    generate_ase(palette, outfile)
    print ('Generated ' + outfile)
    
    # Generate Unity assets
    outfile = os.path.join(outdir, palette['id'] + '.colors')
    generate_unity(palette, outfile)
    print ('Generated ' + outfile)


# Scan palettes directory and build each palette
for dirname, dirs, files in os.walk(INDIR):
    print ('>{}'.format(dirname))
    for filename in glob.glob(os.path.join(dirname, '*.gpl')):
        process_palette (os.path.relpath(filename, INDIR))
