<<<<<<< Updated upstream
#!/usr/bin/env python

=======
#!/usr/bin/env python3
>>>>>>> Stashed changes
from ase import Atoms
from ase.io import read, write
import argparse
import pathlib
import subprocess
from glob import glob
import shutil
from copy_files import copy_cif_file
import tarfile

parser = argparse.ArgumentParser()
parser.add_argument('-i','--InputFolder',
                    type=str,
                    action='store',
                    required=False,
                    metavar='INPUT_FOLDER',
                    default='.',
                    help='Location of the framework CIF files.')

parser.add_argument('-o','--OutputFolder',
                    type=str,
                    action='store',
                    required=False,
                    metavar='OUTPUT_FOLDER',
                    default='.',
                    help='Intended location for output files.')

parser.add_argument('-f','--FrameworkName',
                    type=str,
                    action='store',
                    required=True,
                    metavar='FRAMEWORK_NAME',
                    help='Name of the framework used (associated with the .cif file).')

parser.add_argument('--FrameworkSource',
                    type=str,
                    required=True,
                    action='store',
                    metavar='FRAMEWORK_SOURCE',
                    choices=['local',
                             'CSD',
                             'hMOF',
                             'BWDB',
                             'BW20K',
                             'ARABG',
                             'CoRE2019',
                             'CoRE_DDEC',
                             'CURATED-COF',
                             'baburin_2008',
                             'simperler_2005',
                             'database_zeolite_structures'],
                    help='Source of the CIF file describing the nanoporous material structure.')

parser.add_argument('--FrameworkFolder',
                    type=str,
                    action='store',
                    required=True,
                    metavar='FRAMEWORK_FOLDER',
                    help='Location of the framework <source>/<name>.cif files.')
args = parser.parse_args()

# Copy files to output directory
copy_cif_file(args.FrameworkFolder, args.FrameworkSource, args.FrameworkName, args.OutputFolder)

# Calculate self-consistent properties
input_file = pathlib.Path(args.OutputFolder,  args.FrameworkName).with_suffix('.cif')

target = read(input_file)

output_str = ''
output_str += f'{args.FrameworkName}.xyz' #is this the location  of the file? if so, i need to add outputfolder here
output_str += '\n'
output_str += ' '.join([str(x) for x in target.cell.lengths()])
output_str += '\n'
output_str += ' '.join([str(x) for x in target.cell.angles()])
with open(f'{args.OutputFolder}/input.dat', 'w') as f:
    f.write(output_str)

target.write(f'{args.OutputFolder}/{args.FrameworkName}.xyz', format='xyz')

with tarfile.open(f'{args.OutputFolder}/xyz.tgz', 'w:gz') as tar:
    tar.add(f'{args.OutputFolder}/{args.FrameworkName}.xyz')