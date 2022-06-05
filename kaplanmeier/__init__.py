from kaplanmeier.kaplanmeier import (
    fit,
	plot,
	example_data,
)

__author__ = 'Erdogan Tasksen'
__email__ = 'erdogant@gmail.com'
__version__ = '0.1.7'

# module level doc-string
__doc__ = """
kaplanmeier - This packages computes the log-rank P-value and computes survival curves based on kaplan meier.
===============================================================================================================

**kaplanmeier**
See README.md file for mores information.

Example
----------
>>> # Import library
>>> import kaplanmeier as km
>>>
>>> # Example data
>>> df = km.example_data()
>>>
>>> # Fit
>>> results = km.fit(df['time'], df['Died'], df['group'])
>>>
>>> # Plot
>>> km.plot(results)
>>>
>>> km.plot(results, cmap='Set1', cii_lines='lifelines', cii_alpha=0.05)
>>> km.plot(results, cmap=[(1, 0, 0),(0, 0, 1)])
>>> km.plot(results, cmap='Set1', methodtype='custom')
>>>
>>> results['logrank_P']
>>> results['logrank_Z']

"""
