#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Ed Mountjoy
#
'''
Processes the validated gold-standard jsons. Processing includes:
1. Combining all records into a single file
2. Liftover positions from GRCh37 <-> GRCh38
3. Extract `highest confidence` field
'''

import os
import sys
import json
import argparse
from glob import glob
from pprint import pprint
from pyliftover import LiftOver

def main():

    # Parse args
    args = parse_args()
    confidence_orders = ['High', 'Low'] # Used to sort "highest" confidence

    # Load gold-standards
    gold_standards = load_gold_standards(args.input_pattern)

    # Create liftOver instances from chain files
    if args.grch37_to_38:
        args.grch37_to_38 = LiftOver(args.grch37_to_38)
    if args.grch38_to_37:
        args.grch38_to_37 = LiftOver(args.grch38_to_37)

    # Iterate over and process records
    out_data = []
    for record in gold_standards:

        # Lift-over positions to all assemblies
        record['sentinel_variant'] = fill_in_assemblies(
            record['sentinel_variant'],
            args.grch37_to_38,
            args.grch38_to_37
        )

        # Extract highest confidence
        record['gold_standard_info']['highest_confidence'] = sorted(
            [entry['confidence'] for entry in
             record['gold_standard_info']['evidence']],
            key=lambda x: confidence_orders.index(x)
        )[0]

        out_data.append(record)
    
    # Write output
    if not os.path.exists(os.path.dirname(args.output)):
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as out_h:
        json.dump(out_data, out_h, ensure_ascii=False, indent=2)

    return 0

def fill_in_assemblies(variant_obj, grch37_to_38, grch38_to_37):
    ''' Takes a variant object, then liftsover to GRCh37 and vice versa
    Args:
        variant_obj (dict): sentinel_variant object from gold standard schema
        grch37_to_38_chainfile (pyliftover.LiftOver): liftover object
        grch38_to_37_chainfile (pyliftover.LiftOver): liftover object
    Returns:
        variant_obj (dict)
    '''
    
    # Lift-over GRCh37 to GRCh38
    if (
        (variant_obj.get('locus_GRCh37', None) is not None) and
        (variant_obj.get('locus_GRCh38', None) is None)
        ):

        # Perform liftover
        lo = grch37_to_38.convert_coordinate(
            variant_obj['locus_GRCh37']['chromosome'],
            variant_obj['locus_GRCh37']['position'] - 1
        )

        # Add result to variant_obj
        try:
            variant_obj['locus_GRCh38'] = {
                'chromosome': lo[0][0],
                'position': lo[0][1] + 1
            }
        except IndexError:
            print('WARNING: No locus found in GRCh38 for {} ("{}", {})'.format(
                variant_obj.get('rsid', None),
                variant_obj['locus_GRCh37']['chromosome'],
                variant_obj['locus_GRCh37']['position']
            ))
    
    # Lift-over GRCh38 to GRCh37
    if (
        (variant_obj.get('locus_GRCh38', None) is not None) and
        (variant_obj.get('locus_GRCh37', None) is None)
        ):

        # Perform liftover
        lo = grch38_to_37.convert_coordinate(
            variant_obj['locus_GRCh38']['chromosome'],
            variant_obj['locus_GRCh38']['position'] - 1
        )

        # Add result to variant_obj
        try:
            variant_obj['locus_GRCh37'] = {
                'chromosome': lo[0][0],
                'position': lo[0][1] + 1
            }
        except IndexError:
            print('WARNING: No locus found in GRCh37 for {} ("{}", {})'.format(
                variant_obj.get('rsid', None),
                variant_obj['locus_GRCh38']['chromosome'],
                variant_obj['locus_GRCh38']['position']
            ))
    
    return variant_obj

def load_gold_standards(in_pattern):
    ''' Yields a validated gold-standard one at a time
    Args:
        in_pattern (str): glob pattern for all validated jsons
    Returns:
        yields one records at a time
    '''
    for inf in glob(in_pattern):
        # Load data
        with open(inf, 'r') as in_h:
            data = json.load(in_h)
        # If a list, yield records separately
        if isinstance(data, list):
            for record in data:
                yield record
        # Else return the record itself
        else:
            yield data

def parse_args():
    """ Load command line args """
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_pattern', metavar="<str>",
                        default='../gold_standards/unprocessed_validated/*.json',
                        required=True)
    parser.add_argument('--output', metavar="<file>",
                        type=lambda fn: file_choices(('json'), fn),
                        required=True)
    parser.add_argument('--grch37_to_38', metavar="<file>",
                        help='GRCh37 to GRCh38 chainfile',
                        required=True)
    parser.add_argument('--grch38_to_37', metavar="<file>",
                        help='GRCh38 to GRCh37 chainfile',
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
