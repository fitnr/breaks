#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of breaks.
# https://github.com/fitnr/breaks

# Licensed under the GPL license:
# https://opensource.org/licenses/GPL-3.0
# Copyright (c) 2016, fitnr <contact@fakeisthenewreal.org>

from os import environ
import click
from . import __version__, breaks, METHODS

environ['CPL_MAX_ERROR_REPORTS'] = '5'


@click.command()
@click.argument('infile', metavar='input', type=click.Path(exists=True))
@click.argument('outfile', metavar='output', type=str)
@click.option('-m', '--method', default='quantiles', help='Binning method (default: quantiles)',
              type=click.Choice([m.lower() for m in METHODS]))
@click.option('-f', '--data-field', type=str, metavar='FIELD', required=True, help='data field to read')
@click.option('-b', '--bin-field', type=str, metavar='FIELD', default='bin', help='name of new field')
@click.option('-k', type=int, metavar='COUNT', default=5, help='Number of bins (default: 5)')
@click.option('-w', '--wipe', flag_value=True, default=False, help='Wipe fields besides field and binfield.')
@click.version_option(version=__version__, message='%(prog)s %(version)s')
def main(infile, outfile, method, **kwargs):
    '''Write a geodata file with bins based on a data field'''
    breaks(infile, outfile, method.title(), **kwargs)
