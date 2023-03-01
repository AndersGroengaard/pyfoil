# PyFoil

<p align="center">
 
 
[![Generic badge](https://img.shields.io/badge/Python-3.9-blue)]()
[![Generic badge](https://img.shields.io/badge/version-0.1.0_a-green)]()
</p>


_Repository containing python scripts for generating or fetching various airfoils_

---
Planned features:

* Generate NACA Airfoils
* Fetch historical airfoils
* Create multi-element airfoils.
* Load a datasheet with a timeseries of wind speeds and angles of attacks, and find the best performing airfoil in terms of lift-to-drag ratio.


WORK IN PROGRESS -> Trying to salvage this project from some old local storage at the moment, but will have the full GUI up at some point, hopefully with some improvements :-)
I would like to turn this into a full Python package at some point

Currently, the main window looks like this:

<img src="./doc/gui.png" width="700">


## How to use

```python
from foils import NACA

NACA('2412')
```
