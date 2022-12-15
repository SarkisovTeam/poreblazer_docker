from ase import Atoms
from ase.io import read, write
import argparse
import pathlib
import subprocess
from glob import glob
import shutil

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
                    help='Name of the framework used (and associated .cif file).')

args = parser.parse_args()
input_file = pathlib.Path(args.InputFolder,  args.FrameworkName).with_suffix('.cif')

target = read(input_file)

output_str = ''
output_str += f'{args.FrameworkName}.xyz'
output_str += '\n'
output_str += ' '.join([str(x) for x in target.cell.lengths()])
output_str += '\n'
output_str += ' '.join([str(x) for x in target.cell.angles()])
with open('input.dat', 'w') as f:
    f.write(output_str)

target.write(f'{args.FrameworkName}.xyz', format='xyz')

with open('output.txt', 'w') as output_summary:
    subprocess.run(['./poreblazer.exe', './input.dat'], stdout=output_summary)

outputfiles = glob('*.txt')
for x in outputfiles:
    shutil.copyfile(x, f'./{args.OutputFolder}/{args.FrameworkName}_{x}')
    
shutil.copyfile('summary.dat', f'./{args.OutputFolder}/{args.FrameworkName}_summary.dat')