# breaks

Command line tool for adding data classes to geodata files.

Built on top of [Fiona](http://toblerity.org/fiona/README.html) and [Pysal](http://pysal.readthedocs.org/en/latest/) [mapclassify](http://pysal.org/1.2/library/esda/mapclassify.html).

## Install

Requires [GDAL](http://gdal.org). [Numpy](http://www.numpy.org) and Pysal will be installed if not available.

```
pip install breaks
```

## These are the breaks

Add quintile bins on 'fieldname':
```
breaks data.shp fieldname data_binned.shp
```

This writes a file called `data_binned.shp` which is a copy of `data.shp`, but with an additional `bin` field, which contains a number from 0 to 4 (it will contain `NULL` values for rows with missing data).

Add decile bins on 'fieldname':
```
breaks -k 10 data.shp fieldname data_binned.json
```

Add five [Fisher-Jenks](https://en.wikipedia.org/wiki/Jenks_natural_breaks_optimization) bins on 'fieldname':
```
breaks --method fisher_jenks data.json fieldname data_binned.json
```

Add decile bins on 'fieldname' to a field called 'mybin':
```
breaks --bin-field mybin data.json fieldname data_binned.json
```

Add custom bins on 'fieldname':
```
breaks --bins 50,75,150,250,500 data.json fieldname data_binned.json
```
(Give the upper-bounds as a comma-separated list.)

````
Usage: breaks [OPTIONS] input data-field output

  Write a geodata file with bins based on a data field

Options:
  -m, --method METHOD    Binning method:
                         equal_interval
                         fisher_jenks
                         jenks_caspall
                         jenks_caspall_forced
                         jenks_caspall_sampled
                         max_p_classifier
                         maximum_breaks
                         natural_breaks
                         quantiles (default)
  -b, --bin-field FIELD  name of new field
  -k COUNT               Number of bins (default: 5)
  -B, --bins TEXT        Comma-separated list of breaks (a series of upper-
                         bounds)
  --version              Show the version and exit.
  --help                 Show this message and exit.

````

## License

Copyright 2016 Neil Freeman. Available under the GNU Public License.
