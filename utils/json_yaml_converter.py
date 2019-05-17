#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Ed Mountjoy
#

import sys
import json
import yaml
import argparse

def main():

    # Parse args
    args = parse_args()

    # Get extensions
    in_ext = args.input.split('.')[-1]
    out_ext = args.output.split('.')[-1]

    # Run conversion
    if in_ext == 'json' and out_ext == 'yaml':
        convert_json_to_yaml(args.input, args.output)
    elif in_ext == 'yaml' and out_ext == 'json':
        convert_yaml_to_json(args.input, args.output)
    else:
        sys.exit('Error: source/dest extensions must be json/yaml')

    return 0

def convert_json_to_yaml(inf, outf):
    # Load json
    with open(inf, 'r') as in_h:
        data = json.load(in_h)
    # Write yaml
    with open(outf, 'w') as out_h:
        yaml.dump(data, out_h, allow_unicode=True, default_flow_style=False)

def convert_yaml_to_json(inf, outf):
    # Load json
    with open(inf, 'r') as in_h:
        data = yaml.load(in_h)
    # Write yaml
    with open(outf, 'w') as out_h:
        json.dump(data, out_h,  ensure_ascii=False, indent=2)

def parse_args():
    """ Load command line args """
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', metavar="<file>", type=str, required=True)
    parser.add_argument('--output', metavar="<file>", type=str, required=True)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()
