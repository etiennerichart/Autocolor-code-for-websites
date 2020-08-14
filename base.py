#!/usr/bin/python

import sys, argparse
from python_code import PythonCode

if sys.platform == 'win32':
    prefix_cahracter = '/'
else:
    prefix_cahracter = '-'
parser = argparse.ArgumentParser(prog='autocolor-code-for-websites',
                    description='Take code and the programming language to color the code.',
                    epilog='Enjoy!',
                    prefix_chars=prefix_cahracter)
parser.add_argument('language',
                    type=str,
                    choices=['python'],
                    action='store',
                    nargs='?',
                    default='python',
                    help='the language the code is written in')
parser.add_argument('file',
                    type=argparse.FileType('r'),
                    nargs=argparse.REMAINDER,
                    help='the files you wish to ')
args = parser.parse_args(['python', './python_code.py', 'base.py'])

if args.language == 'python':
    for file in args.file:
       PythonCode(file)
