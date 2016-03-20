#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of breaks.
# https://github.com/fitnr/breaks

# Licensed under the GPL license:
# https://opensource.org/licenses/GPL-3.0
# Copyright (c) 2016, Neil Freeman <contact@fakeisthenewreal.org>
from __future__ import print_function
import sys
from os import environ
import click
from . import __version__, LOWER_METHODS, breaks


@click.command()
@click.argument('infile', metavar='input', type=click.Path(exists=True))
@click.argument('data-field', type=str, metavar='data-field')
@click.argument('outfile', metavar='output', type=click.Path(writable=True, allow_dash=True))
@click.option('-m', '--method', metavar='METHOD', default='quantiles', type=click.Choice(LOWER_METHODS),
              help='Binning method:\n' + '\n'.join(LOWER_METHODS) + ' (default)')
@click.option('-b', '--bin-field', type=str, metavar='FIELD', default='bin', help='name of new field')
@click.option('-n', '--norm-field', type=str, metavar='FIELD', default=None,
              help='Normalize (divide) bin-field by this name field')
@click.option('-k', type=int, metavar='COUNT', default=5, help='Number of bins (default: 5)')
@click.option('-B', '--bins', type=str, help='Comma-separated list of breaks (a series of upper-bounds)')
@click.option('-i', '--id-field', type=str, metavar='FIELD', default=None,
              help='If given, only write this field, bin-field, and data-field (and norm-field, if given).')
@click.version_option(version=__version__, message='%(prog)s %(version)s')
def main(infile, outfile, **kwargs):
    '''Write a geodata file with bins based on a data field.'''
    # Set OGR error reporting limit
    environ['CPL_MAX_ERROR_REPORTS'] = environ.get('CPL_MAX_ERROR_REPORTS', '5')

    result = breaks(infile, outfile, **kwargs)

    print(result, file=sys.stderr)
