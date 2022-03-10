from kaplanmeier.kaplanmeier import (
    fit,
	plot,
	example_data,
)

__author__ = 'Erdogan Tasksen'
__email__ = 'erdogant@gmail.com'
__version__ = '0.1.5'

# module level doc-string
__doc__ = """
kaplanmeier - This packages computes the log-rank P-value and computes survival curves based on kaplan meier.
===============================================================================================================

**kaplanmeier**
See README.md file for mores information.

Example
----------
>>> import kaplanmeier as km
>>> df = km.example_data()
>>> out = km.fit(df['time'], df['Died'], df['group'])
>>> km.plot(out)

>>> km.plot(out, cmap='Set1', cii_lines=True, cii_alpha=0.05)
>>> km.plot(out, cmap=[(1, 0, 0),(0, 0, 1)])
>>> km.plot(out, cmap='Set1', methodtype='custom')

"""
