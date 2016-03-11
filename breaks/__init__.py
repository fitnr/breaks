#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of breaks.
# https://github.com/fitnr/breaks

# Licensed under the GPL license:
# https://opensource.org/licenses/GPL-3.0
# Copyright (c) 2016, fitnr <contact@fakeisthenewreal.org>

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


def make_meta(source, outfile, bin_field):
    meta = {
        'crs': source.crs,
        'driver': fionautil.drivers.from_path(outfile),
        'schema': source.schema,
    }
    meta['schema']['properties'][bin_field] = 'int'

    return meta


def breaks(infile, outfile, method, data_field, k=None, **kwargs):
    k = k or 5
    bin_field = kwargs.pop('bin_field', 'bin')

    if kwargs.get('bins'):
        method = 'User_Defined'
        k = kwargs.pop('bins')

    with fiona.drivers():
        with fiona.open(infile) as source:
            meta = make_meta(source, outfile, bin_field)
            contents = list(source)
            data = [f['properties'][data_field] for f in contents if f['properties'][data_field] is not None]
            classes = getattr(mapclassify, method)(np.array(data), k)

        k = len(classes.bins) - 1

        with fiona.open(outfile, 'w', **meta) as sink:
            for f in contents:
                value = f['properties'][data_field]
                if value is None:
                    f['properties'][bin_field] = None
                else:
                    f['properties'][bin_field] = min(k, bisect_left(classes.bins, value))

                sink.write(f)

    return classes
