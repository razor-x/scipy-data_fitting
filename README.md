# Data Fitting with SciPy

[![PyPI Version](http://img.shields.io/pypi/v/scipy-data_fitting.svg)](https://pypi.python.org/pypi/scipy-data_fitting)
[![MIT License](http://img.shields.io/badge/license-MIT-red.svg)](./LICENSE.txt)

![fit plot](https://raw.github.com/razor-x/scipy-data_fitting/master/plot.png)

Check out the [example fits on Fitalyzer](http://io.evansosenko.com/fitalyzer/?firebase=scipy-data-fitting).
See the [Fitalyzer README](https://github.com/razor-x/fitalyzer) for details on how to use Fitalyzer for visualizing your fits.

## Documentation

Documentation generated from source with
[pdoc](https://pypi.python.org/pypi/pdoc/)
for the latest version is hosted at
[packages.python.org/scipy-data_fitting/](http://packages.python.org/scipy-data_fitting/).

To get started quickly, check out the
[examples](https://github.com/razor-x/scipy-data_fitting/tree/master/examples).

Then, refer to the source documentation for details on how to use each class.

## Basic usage

````python
from scipy_data_fitting import Data, Model, Fit, Plot

# Load data from a CSV file.
data = Data('linear')
data.path = 'linear.csv'
data.error = (0.5, None)

# Create a linear model.
model = Model('linear')
model.add_symbols('t', 'v', 'x_0')
t, v, x_0 = model.get_symbols('t', 'v', 'x_0')
model.expressions['line'] = v * t + x_0

# Create the fit using the data and model.
fit = Fit('linear', data=data, model=model)
fit.expression = 'line'
fit.independent = {'symbol': 't', 'name': 'Time', 'units': 's'}
fit.dependent = {'name': 'Distance', 'units': 'm'}
fit.parameters = [
    {'symbol': 'v', 'guess': 1, 'units': 'm/s'},
    {'symbol': 'x_0', 'value': 1, 'units': 'm'},
]

# Save the fit result to a json file.
fit.to_json(fit.name + '.json', meta=fit.metadata)

# Save a plot of the fit to an image file.
plot = Plot(fit)
plot.save(fit.name + '.svg')
plot.close()
````

### Controlling the fitting process

The above example will fit the line using the default algorithm
[`scipy.optimize.curve_fit`](http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html).

For a linear fit, it may be more desirable to use a more efficient algorithm.

For example, to use
[`numpy.polyfit`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.polyfit.html),
one could set a `fit_function` and allow both parameters to vary,

````python
fit.parameters = [
    {'symbol': 'v', 'guess': 1, 'units': 'm/s'},
    {'symbol': 'x_0', 'guess': 1, 'units': 'm'},
]
fit.options['fit_function'] = lambda f, x, y, p0, **op: (numpy.polyfit(x, y, 1), )
````

Controlling the fitting process this way allows, for example, incorporating error values
and computing and returning goodness of fit information.

See [`scipy_data_fitting.Fit.options`](http://packages.python.org/scipy-data_fitting/#scipy_data_fitting.Fit.options)
for further details on how to control the fit and also how to use [lmfit](http://lmfit.github.io/lmfit-py/).

## Installation

This package is registered on the Python Package Index (PyPI) at
[pypi.python.org/pypi/scipy-data_fitting](https://pypi.python.org/pypi/scipy-data_fitting).

Add this line to your application's `requirements.txt`:

````
scipy-data_fitting
````

And then execute:

````bash
$ pip install -r requirements.txt
````

Or install it yourself as:

````bash
$ pip install scipy-data_fitting
````

Instead of the package name `scipy-data_fitting`,
you can use this repository directly with

````
git+https://github.com/razor-x/scipy-data_fitting.git@master#egg=scipy-data_fitting
````

## Development

### Source Repository

The [source](https://github.com/razor-x/scipy-data_fitting) is hosted at GitHub.
Fork it on GitHub, or clone the project with

````bash
$ git clone https://github.com/razor-x/scipy-data_fitting.git
````

### Documentation

Generate documentation with pdoc by running

````bash
$ make docs
````

### Tests

Run the tests with

````bash
$ make tests
````

### Examples

Run an example with

````bash
$ python examples/example_fit.py
````

or run all the examples with

````bash
$ make examples
````

## License

This code is licensed under the MIT license.

## Warranty

This software is provided "as is" and without any express or
implied warranties, including, without limitation, the implied
warranties of merchantibility and fitness for a particular
purpose.
