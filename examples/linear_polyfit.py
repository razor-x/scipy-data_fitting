import os
import numpy
from example_helper import save_example_fit
from scipy_data_fitting import Data, Model, Fit

#
# Example of a basic linear fit.
# This example demonstrates how to use a custom `fit_function`.
#

name = 'linear_polyfit'

# Load data from a csv file.
data = Data(name)
data.path = os.path.join('examples', 'data', 'linear.csv')
data.genfromtxt_args['skip_header'] = 1

# Create a linear model.
model = Model(name)
model.add_symbols('t', 'v', 'x_0')
t, v, x_0 = model.get_symbols('t', 'v', 'x_0')
model.expressions['line'] = v * t + x_0

# Create the fit using the data and model.
fit = Fit(name, data=data, model=model)
fit.expression = 'line'
fit.independent = {'symbol': 't', 'name': 'Time', 'units': 's'}
fit.dependent = {'name': 'Distance', 'units': 'm'}
fit.parameters = [
    {'symbol': 'v', 'guess': 1, 'units': 'm/s'},
    {'symbol': 'x_0', 'guess': 1, 'units': 'm'},
]

# Use `numpy.polyfit` to do the fit.
fit.options['fit_function'] = lambda f, x, y, p0, **op: (numpy.polyfit(x, y, 1), )

# Save the fit to disk.
save_example_fit(fit)
