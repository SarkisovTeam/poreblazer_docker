#!/usr/bin/env python3
import argparse
import subprocess
from glob import glob
import shutil
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
                    help='Name of the framework used (and associated .cif file).')

args = parser.parse_args()

with tarfile.open(f'{args.OutputFolder}/xyz.tgz', 'r:gz') as tar:
    tar.extract(f'{args.OutputFolder}/{args.FrameworkName}.xyz')

# shutil.copyfile(f'{args.InputFolder}/{args.FrameworkName}.xyz', f'/run/{args.FrameworkName}.xyz')

with open(f'./output.txt', 'w') as output_summary:
    subprocess.run(['/run/poreblazer.exe', f'{args.InputFolder}/input.dat'], stdout=output_summary)

outputfiles = glob('*.txt')
for x in outputfiles:
    shutil.copyfile(x, f'{args.OutputFolder}/{args.FrameworkName}_{x}')
    
shutil.copyfile('/run/summary.dat', f'{args.OutputFolder}/{args.FrameworkName}_summary.dat')

with tarfile.open(f'{args.OutputFolder}/summary.tgz', 'w:gz') as tar:
    tar.add(f'{args.OutputFolder}/{args.FrameworkName}_summary.dat')
    for x in outputfiles:
        tar.add(f'{args.OutputFolder}/{args.FrameworkName}_{x}')