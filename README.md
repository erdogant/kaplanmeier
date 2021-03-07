# kaplanmeier - Python package to compute the kaplan meier curves, log-rank test, and make the plots.

[![Python](https://img.shields.io/pypi/pyversions/kaplanmeier)](https://img.shields.io/pypi/pyversions/kaplanmeier)
[![PyPI Version](https://img.shields.io/pypi/v/kaplanmeier)](https://pypi.org/project/kaplanmeier/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/erdogant/kaplanmeier/blob/master/LICENSE)
[![Coffee](https://img.shields.io/badge/coffee-black-grey.svg)](https://erdogant.github.io/donate/?currency=USD&amount=5)
[![Github Forks](https://img.shields.io/github/forks/erdogant/kaplanmeier.svg)](https://github.com/erdogant/kaplanmeier/network)
[![GitHub Open Issues](https://img.shields.io/github/issues/erdogant/kaplanmeier.svg)](https://github.com/erdogant/kaplanmeier/issues)
[![Project Status](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)
[![Downloads](https://pepy.tech/badge/kaplanmeier/month)](https://pepy.tech/project/kaplanmeier/)
[![Downloads](https://pepy.tech/badge/kaplanmeier)](https://pepy.tech/project/kaplanmeier)
[![Sphinx](https://img.shields.io/badge/Sphinx-Docs-Green)](https://erdogant.github.io/kaplanmeier/)

    Star it if you like it!

## Installation
* Install kaplanmeier from PyPI (recommended). kaplanmeier is compatible with Python 3.6+ and runs on Linux, MacOS X and Windows. 
* Distributed under the MIT license.

## Requirements
* Create environment:
```python
conda create -n env_KM python=3.6
conda activate env_KM
pip install matplotlib numpy pandas seaborn lifelines
```

## Installation
```
pip install kaplanmeier
```
#### Import kaplanmeier package
```python
import kaplanmeier as km
```

#### Example:
```python
df = km.example_data()
time_event=df['time']
censoring=df['Died'] 
labx=df['group']

# Compute survival
out=km.fit(time_event, censoring, labx)
```

#### Make figure with cii_alpha=0.05 (default)
```python
km.plot(out)
```
<p align="center">
  <img src="https://github.com/erdogant/kaplanmeier/blob/master/docs/figs/fig2.png" width="600" />
</p>

```python
km.plot(out, cmap='Set1', cii_lines=None, cii_alpha=0.05)
```
<p align="center">
  <img src="https://github.com/erdogant/kaplanmeier/blob/master/docs/figs/fig1.png" width="600" />
</p>

```python
km.plot(out, cmap='Set1', cii_lines='line', cii_alpha=0.05)
```
<p align="center">
  <img src="https://github.com/erdogant/kaplanmeier/blob/master/docs/figs/fig3.png" width="600" />
</p>

```python
km.plot(out, cmap=[(1, 0, 1),(0, 1, 1)])
```
<p align="center">
  <img src="https://github.com/erdogant/kaplanmeier/blob/master/docs/figs/fig4.png" width="600" />
</p>

```python
km.plot(out, cmap='Set2')
```
<p align="center">
  <img src="https://github.com/erdogant/kaplanmeier/blob/master/docs/figs/fig5.png" width="600" />
</p>

```python
km.plot(out, cmap='Set2', methodtype='custom')
```
<p align="center">
  <img src="https://github.com/erdogant/kaplanmeier/blob/master/docs/figs/fig6.png" width="600" />
</p>



* df looks like this:
```
     time  Died  group
0     485     0      1
1     526     1      2
2     588     1      2
3     997     0      1
4     426     1      1
..    ...   ...    ...
175   183     0      1
176  3196     0      1
177   457     1      2
178  2100     1      1
179   376     0      1

[180 rows x 3 columns]
```

### Citation
Please cite kaplanmeier in your publications if this is useful for your research. Here is an example BibTeX entry:
```BibTeX
@misc{erdogant2019kaplanmeier,
  title={kaplanmeier},
  author={Erdogan Taskesen},
  year={2019},
  howpublished={\url{https://github.com/erdogant/kaplanmeier}},
}
```

## References
* http://lifelines.readthedocs.io/en/latest/Survival%20analysis%20with%20lifelines.html


### Maintainer
* Erdogan Taskesen, github: [erdogant](https://github.com/erdogant)
* Contributions are welcome.
* If you wish to buy me a <a href="https://erdogant.github.io/donate/?currency=USD&amount=5">Coffee</a> for this work, it is very appreciated :)
