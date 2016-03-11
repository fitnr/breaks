# This file is part of breaks.
# https://github.com/fitnr/breaks

# Licensed under the GPL license:
# https://opensource.org/licenses/GPL-3.0
# Copyright (c) 2016, Neil Freeman <contact@fakeisthenewreal.org>

.PHONY: test

test:
	coverage run --include='breaks/*' setup.py test
	coverage report
	coverage html

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
