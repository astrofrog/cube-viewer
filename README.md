About
-----

This is an experimental package to show isocontours of FITS spectral cubes using VTK and Qt. This can be used either as a standalone tool, or as a [glue](http://www.glueviz.org) data viewer.

Dependencies
------------

The following dependencies are required:

* [Numpy](http://www.numpy.org)
* [Astropy](http://www.astropy.org)
* [spectral-cube](http://spectral-cube.readthedocs.org)
* [PyQt4](http://www.riverbankcomputing.co.uk/software/pyqt/intro)
* [VTK](http://www.vtk.org/)
* [Palettable](https://jiffyclub.github.io/palettable/)
* [six](https://pypi.python.org/pypi/six)
* [glue](https://www.glueviz.org)

You can easily create a conda environment with these dependencies using:

```
conda create -n vtk-viewer-test python=2.7 --yes
source activate vtk-viewer-test
conda install pyqt vtk numpy astropy pip --yes
pip install spectral_cube palettable
```

[Anaconda](https://store.continuum.io/cshop/anaconda/) or [Miniconda](http://conda.pydata.org/miniconda.html) are highly recommended since VTK and PyQt4 are tricky dependencies to install.

Using as a standalone tool
--------------------------

To run:

```
cube-viewer filename [levels] [--stretch-spectral=value]
```

e.g.

```
cube-viewer ../L1448_13CO.fits 1 2 3 4 5 --stretch-spectral=2.
```

![screenshot](screenshot.png)

Using as a Glue plugin
----------------------

To use this as a glue plugin, install this package, then add the following to your glue ``config.py`` file::

    from glue.config import qt_client
    qt_client.lazy_add('cube_viewer.glue_plugin')

At the moment, this only supports viewing of the main data in a cube, and does not show subsets.
