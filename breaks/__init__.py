#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of breaks.
# https://github.com/fitnr/breaks

# Licensed under the GPL license:
# https://opensource.org/licenses/GPL-3.0
# Copyright (c) 2016, Neil Freeman <contact@fakeisthenewreal.org>

from bisect import bisect_left
import numpy as np
import fiona
import fionautil.drivers
from pysal.esda import mapclassify

__version__ = '0.1.0'

METHODS = (
    'Equal_Interval',
    'Fisher_Jenks',
    'Jenks_Caspall',
    'Jenks_Caspall_Forced',
    'Jenks_Caspall_Sampled',
    'Max_P_Classifier',
    'Maximum_Breaks',
    'Natural_Breaks',
    'Quantiles',
)


def bisect(bins, value):
    if value is None:
        return None
    return bisect_left(bins, value)


def write(outfile, features, **kwargs):
    kwargs['driver'] = fionautil.drivers.from_path(outfile)
    with fiona.open(outfile, 'w', **kwargs) as sink:
        sink.writerecords(features)


def breaks(infile, outfile, method, data_field, k=None, bin_field=None, **kwargs):
    '''
    Calculate bins on <infile> via <method>.

    Args:
        infile (str): path
        outfile (str): path
        method (str): a valid pysal.esda.mapclassify method
        data_field (str): field in <infile> to read
        k (int): number of bins to create (default: 5)
        bin_field (str): field in <outfile> to create (default: bin)
        bins (list): Upper bounds of bins to use in User_Defined classifying.
                     Overrides method and k.

    Returns:
        mapclassify bins instance
    '''
    k = k or 5
    bin_field = 'bin' or bin_field

    if kwargs.get('bins'):
        method = 'User_Defined'
        k = kwargs.pop('bins')

    classify = getattr(mapclassify, method)

    with fiona.drivers():
        with fiona.open(infile) as source:
            meta = {
                'schema': source.schema,
                'crs': source.crs,
            }

            if data_field not in source.schema['properties']:
                raise ValueError('data field not found: {}'.format(data_field))

            features = list(source)
            data = [f['properties'][data_field] for f in features if f['properties'][data_field] is not None]
            classes = classify(np.array(data), k)

        for f in features:
            f['properties'][bin_field] = bisect(classes.bins, f['properties'][data_field])

        meta['schema']['properties'][bin_field] = 'int'
        write(outfile, features, **meta)

    return classes
