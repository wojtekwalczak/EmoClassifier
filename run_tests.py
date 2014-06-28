#!/usr/bin/env python

import sys
import unittest

suite = unittest.TestLoader().discover('test')
results = unittest.TextTestRunner(verbosity=2).run(suite)
if len(results.errors) > 0 or len(results.failures) > 0:
   sys.exit(1)
