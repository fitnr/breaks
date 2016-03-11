#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of breaks.
# https://github.com/fitnr/breaks

# Licensed under the GPL license:
# https://opensource.org/licenses/GPL-3.0
# Copyright (c) 2016, fitnr <contact@fakeisthenewreal.org>
from bisect import bisect_right
import argparse
import numpy as np
import fionautil.drivers
from pysal.esda import mapclassify
import fiona


METHODS = (
    'Box_Plot',
    'Equal_Interval',
    'Fisher_Jenks',
    'Jenks_Caspall',
    'Jenks_Caspall_Forced',
    'Jenks_Caspall_Sampled',
    'Max_P_Classifier',
    'Maximum_Breaks',
    'Natural_Breaks',
    'Quantiles',
    'Percentiles',
    'Std_Mean',
)


def write_breaks(outfile, infile, field, method, k, binfield):
    classify = getattr(mapclassify, method)

    with fiona.drivers():
        with fiona.open(infile) as source:

            meta = {
                'crs': source.crs,
                'driver': fionautil.drivers.from_path(outfile),
                'schema': source.schema,
            }

            meta['schema']['properties'][binfield] = 'int'

            contents = list(source)

        array = np.array([f['properties'][field] or np.nan for f in contents])
        breaks = classify(array, k)

        with fiona.open(outfile, 'w', **meta) as sink:
            for f in contents:
                f['properties'][binfield] = bisect_right(breaks.bins, f['properties'][field])
                sink.write(f)


def main():
    lower_methods = tuple(b.lower() for b in METHODS)

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str)
    parser.add_argument('-f', '--field', type=str, required=True)
    parser.add_argument('-m', '--method', type=str, choices=lower_methods)
    parser.add_argument('-k', '--count', type=int, default=5, dest='k', help='Number of bins. Default: 5')
    parser.add_argument('-b', '--binfield', type=str, default='bin', help='Name of the new field')
    parser.add_argument('outfile', type=str)

    args = vars(parser.parse_args())

    args['method'] = METHODS[lower_methods.index(args['method'])]

    write_breaks(**args)


if __name__ == '__main__':
    main()
