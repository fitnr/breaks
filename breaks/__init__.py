#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of breaks.
# https://github.com/fitnr/breaks

# Licensed under the GPL license:
# https://opensource.org/licenses/GPL-3.0
# Copyright (c) 2016, Neil Freeman <contact@fakeisthenewreal.org>

from bisect import bisect_left
from collections import OrderedDict
import numpy as np
import fiona
import fionautil.drivers
from pysal.esda import mapclassify

__version__ = '0.2.0'

LOWER_METHODS = (
    'equal_interval',
    'fisher_jenks',
    'jenks_caspall',
    'jenks_caspall_forced',
    'jenks_caspall_sampled',
    'max_p_classifier',
    'maximum_breaks',
    'natural_breaks',
    'quantiles',
)


def bisect(bins, value):
    '''Bisect left, returning None if value is None.'''
    if value is None:
        return None
    return bisect_left(bins, value)


def write(outfile, features, **kwargs):
    '''Use Fiona to write features to <outfile>. Kewyord args should be Fiona meta arguments.'''
    kwargs['driver'] = fionautil.drivers.from_path(outfile)
    with fiona.open(outfile, 'w', **kwargs) as sink:
        sink.writerecords(features)


def getter(data_field, norm_field=None):
    '''Returns a function for getting data value from a feature.'''
    if norm_field:
        def get(f):
            try:
                return float(f['properties'][data_field]) / float(f['properties'][norm_field])
            except TypeError:
                return None
    else:
        def get(f):
            return f['properties'][data_field]

    return get


def setter(bins, data_field, bin_field, **kwargs):
    '''Returns a function for creating an output feature.'''
    norm_field = kwargs.get('norm_field')
    id_field = kwargs.get('id_field')

    get = getter(data_field, norm_field)

    def _set(feature):
        f = {
            'properties': {},
            'geometry': feature['geometry']
        }

        if id_field:
            f['properties'][id_field] = feature['properties'][id_field]
            f['properties'][data_field] = feature['properties'][data_field]

            if norm_field:
                f['properties'][norm_field] = feature['properties'][norm_field]
        else:
            f['properties'] = feature['properties']

        f['properties'][bin_field] = bisect(bins, get(feature))

        return f

    return _set


def binfeatures(features, method, data_field, k, bin_field=None, **kwargs):
    '''Classify input features according to <method>'''
    bin_field = 'bin' or bin_field

    if kwargs.get('bins'):
        method = 'User_Defined'
        k = kwargs.pop('bins')

    classify = getattr(mapclassify, method)

    get = getter(data_field, kwargs.get('norm_field'))

    data = (get(f) for f in features)

    return classify(np.array([d for d in data if d is not None]), k)


def get_features(infile, fields=None):
    '''
    Return the features of <infile>. Includes error checking that given fields exist.

    Args:
        infile (str): path
        fields (Sequence/Generator): Check that these fields exist in <infile>.
                            Raises ValueError if one doesn't appear.

    Returns:
        (tuple) list of features and Fiona metadata for <infile>
    '''
    fields = fields or []
    with fiona.drivers():
        with fiona.open(infile) as source:
            try:
                for f in fields:
                    assert f in source.schema['properties']
            except AssertionError:
                raise ValueError('field not found in {}: {}'.format(infile, f))

            meta = {
                'schema': source.schema,
                'crs': source.crs,
            }

            features = list(source)

    return features, meta


def breaks(infile, outfile, method, data_field, **kwargs):
    '''
    Calculate bins on <infile> via <method>, writing result to <outfile>.
    This is essentially a wrapper for what the breaks CLI does.

    Args:
        infile (str): path to input file
        outfile (str): path to output file
        method (str): a valid pysal.esda.mapclassify method
        data_field (str): field in <infile> to read
        k (int): number of bins to create (default: 5)
        bin_field (str): field in <outfile> to create (default: bin)
        bins (list): Upper bounds of bins to use in User_Defined classifying.
                     Overrides method and k.
        norm_field (str): Field to divide data_field by (both will be coerced to float).

    Returns:
        mapclassify bins instance
    '''
    if kwargs.get('bins'):
        kwargs['bins'] = sorted(float(x) for x in kwargs['bins'].split(','))

    bin_field = kwargs.pop('bin_field', 'bin')
    id_field = kwargs.get('id_field')
    norm_field = kwargs.get('norm_field')
    kwargs['k'] = kwargs.get('k', 5)

    fields = [f for f in (data_field, id_field, norm_field) if f is not None]
    features, meta = get_features(infile, fields)

    if id_field:
        p = meta['schema']['properties']
        meta['schema']['properties'] = OrderedDict((k, v) for k, v in p.items() if k in fields)

    meta['schema']['properties'][bin_field] = 'int'

    classes = binfeatures(features, method.title(), data_field, **kwargs)

    create = setter(classes.bins, data_field, bin_field, id_field=id_field, norm_field=norm_field)

    new_features = (create(f) for f in features)
    write(outfile, new_features, **meta)

    return classes
