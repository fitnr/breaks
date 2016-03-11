# This file is part of breaks.
# https://github.com/fitnr/breaks

# Licensed under the GPL license:
# https://opensource.org/licenses/GPL-3.0
# Copyright (c) 2016, Neil Freeman <contact@fakeisthenewreal.org>

CPL_MAX_ERROR_REPORTS = 0
export CPL_MAX_ERROR_REPORTS

TIGER = http://www2.census.gov/geo/tiger

.PHONY: test deploy

test:
	coverage run --include='breaks/*' setup.py test
	coverage report
	coverage html

bins.json bins.shp: State_2010Census_DP1.shp
	breaks $< DP0180001 $@

State_2010Census_DP1.shp: State_2010Census_DP1.zip
	unzip -qod . $< '$(basename $<).*'
	@touch $@

State_2010Census_DP1.zip: ; curl -O $(TIGER)/TIGER2010DP1/$@

deploy: README.rst
	python setup.py register
	git push
	git push --tags
	rm -rf dist build
	python3 setup.py bdist_wheel --universal
	twine upload dist/*

README.rst: README.md
	- pandoc $< -o $@
	@touch $@
	python setup.py check -r -s -m -q
