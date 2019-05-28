#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Ed Mountjoy
#

import os
import sys
import json
import yaml
import argparse
import pandas as pd
from collections.abc import MutableMapping

def main():

    # Parse args
    args = parse_args()

    # Load json
    in_data = load_input(args.input)
    assert isinstance(in_data, list)

    # Flatten the input data
    out_data = []
    for row in in_data:
        out_data.append(
            flatten_dict(
                row,
                key_sep=args.key_sep,
                list_sep=args.list_sep
            )
        )
    
    # Output flattened file
    df = pd.DataFrame.from_dict(
        out_data
    )
    df.to_csv(args.output, sep=args.output_sep, index=None)

    return 0

def flatten_dict(d, parent_key='', key_sep='.', list_sep='|'):
    ''' Flattens dictionary
    '''
    items = []
    for k, v in d.items():
        new_key = parent_key + key_sep + k if parent_key else k

        # If its a list, flatten
        if isinstance(v, list):
            v = flatten_list(v, list_sep)
            # Skip None items
            if v is None:
                continue 
        # Flatten the dict
        if isinstance(v, MutableMapping):
            items.extend(
                flatten_dict(
                    v, new_key,
                    key_sep=key_sep,
                    list_sep=list_sep
                ).items()
            )
        # Add flattened item
        else:
            items.append((new_key, v))
    return dict(items)

def flatten_list(l, sep):
    ''' Flattens a list
    '''
    # If the list is empty return None
    if len(l) == 0:
        return None
    # If it is a list of dicts
    elif isinstance(l[0], MutableMapping):
        flat_d = {}
        # Get all dict keys
        keys = set([item for sublist in l for item in sublist])
        # Flatten each key separately
        for key in keys:
            flat_d[key] = sep.join(
                [str(entry[key]) for entry in l]
            )
        return flat_d
    # If not a dict, join list
    else:
        return sep.join([str(x) for x in l])

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
                        type=lambda fn: file_choices(('json', 'yaml'), fn),
                        required=True)
    parser.add_argument('--output_sep', metavar="<str>",
                        type=str,
                        help='Output separator',
                        default='\t',
                        required=False)
    parser.add_argument('--list_sep', metavar="<str>",
                        type=str,
                        help='List separator',
                        default='|',
                        required=False)
    parser.add_argument('--key_sep', metavar="<str>",
                        type=str,
                        help='Key separator',
                        default='.',
                        required=False)
    parser.add_argument('--output', metavar="<file>",
                        type=lambda fn: file_choices(('tsv', 'csv'), fn),
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
