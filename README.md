

<div align="center">
 
 <h1 align="center">  PyFoil </h1>
  <a href="https://github.com/AndersGroengaard/pyfoil/issues/new?assignees=&labels=bug&template=01_BUG_REPORT.md&title=bug%3A+">Report a Bug</a>
  ·
  <a href="https://github.com/AndersGroengaard/pyfoil/issues/new?assignees=&labels=enhancement&template=02_FEATURE_REQUEST.md&title=feat%3A+">Request a Feature</a>
  .
  <a href="https://github.com/AndersGroengaard/pyfoil/discussions">Ask a Question</a>
</div>

<br/>


<center>

[![Generic badge](https://img.shields.io/badge/Python-3.9-blue)]()
[![Generic badge](https://img.shields.io/badge/version-0.1.0_a-green)]()

</center>

<br /><br />
_Repository containing python scripts for generating or fetching various airfoils_

 

<!-- TABLE OF CONTENTS -->
<h2 id="table-of-contents"> :book: Table of Contents</h2>

<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about"> ➤ About The Project</a></li>
    <li><a href="#features"> ➤ Features</a></li>
    <li><a href="#planned-features"> ➤ Planned Features</a></li>
     <li><a href="#limitations"> ➤ Limitations</a></li>
  </ol>
</details>
 
<!-- ABOUT THE PROJECT -->
<h2 id="about"> :clipboard: About</h2>
 
<p align="justify"> 
   The intended purpose of this package is to serve as a tool to find the best airfoil shape for your engineering application.
</p>





<br/><br/>


<!-- Features -->
<h2 id="features"> :dart: FEATURES </h2>
* Generate NACA Airfoils

<!-- Features -->
<h2 id="planned-features"> :goal_net: PLANNED FEATURES </h2>

* Fetch historical airfoils
* Create multi-element airfoils.
* Load a datasheet with a timeseries of wind speeds and angles of attacks, and find the best performing airfoil in terms of lift-to-drag ratio.

<!-- Limitations -->
<h2 id="limitations"> :warning: Limitations</h2>
 
<p align="justify"> 
   WORK IN PROGRESS -> Trying to salvage this project from some old local storage at the moment, but will have the full GUI up at some point, hopefully with some improvements :-)
I would like to turn this into a full Python package at some point
</p>



Currently, the main window looks like this:

<img src="./doc/gui.png" width="700">


<br/><br/>

## How to use

To create a 4 and 5 digit NACA airfoils, plotting them and saving them, you could write (See also the examply.py file):

```python

from naca import NACA

# NACA 4-Digit airfoil:
airfoil = NACA("2310")
airfoil.plot()
airfoil.save()


# NACA 5-Digit airfoil:
airfoil = NACA("23116")
airfoil.plot()
airfoil.save()
 
```
