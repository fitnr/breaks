#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of breaks.
# https://github.com/fitnr/breaks

# Licensed under the GPL license:
# https://opensource.org/licenses/GPL-3.0
# Copyright (c) 2016, Neil Freeman <contact@fakeisthenewreal.org>

import unittest
import breaks


class TestCase(unittest.TestCase):

    def testBreaks(self):
        assert breaks.bisect([1, 10, 20, 30], 25) == 3
        assert breaks.bisect([1, 10, 20, 30], None) is None

if __name__ == '__main__':
    unittest.main()
