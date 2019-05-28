#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Ed Mountjoy
#

import os
import sys
import json
import argparse


def main():

    # Parse args
    args = parse_args()

    # Load json
    data = load_input(args.input)
    assert isinstance(data, list)

    # Convert to lines
    with open(args.output, 'w') as out_h:
        for record in data:
            out_h.write(json.dumps(record) + '\n')

    return 0


def load_input(inf):
    ''' Loads the input json or yaml data
    '''
    ext = inf.split('.')[-1]
    if ext == 'json':
        with open(inf, 'r') as in_h:
            data = json.load(in_h)
    elif ext == 'yaml':
        with open(inf, 'r') as in_h:
            data = yaml.load(in_h, Loader=yaml.FullLoader)
    else:
        sys.exit('Error, --input extension not allowed')
    return data

def parse_args():
    """ Load command line args """
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', metavar="<file>",
                        type=lambda fn: file_choices(('json'), fn),
                        required=True)
    parser.add_argument('--output', metavar="<file>",
                        type=lambda fn: file_choices(('jsonl'), fn),
                        required=True)
    args = parser.parse_args()
    return args

def file_choices(choices, fname):
    ext = os.path.splitext(fname)[1][1:]
    if ext not in choices:
       parser.error("file doesn't end with one of {}".format(choices))
    return fname

if __name__ == '__main__':
    main()
