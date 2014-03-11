import os
from example_helper import save_example_fit
from scipy_data_fitting import Data, Model, Fit

#
# Example of a basic linear fit.
# This example demonstrates how to use `prefix` for unit conversions.
#

name = 'linear_scaled'

# Load data from a csv file.
data = Data(name)
data.path = os.path.join('examples','data', 'linear.csv')
data.genfromtxt_args['skip_header'] = 1

# Assume the data was not saved in SI base units.
data.scale = ('micro', 'kilo')

# Create a linear model.
model = Model(name)
model.add_symbols('t', 'v', 'x_0')
t, v, x_0 = model.get_symbols('t', 'v', 'x_0')
model.expressions['line'] = v * t + x_0

# Create the fit using the data and model.
fit = Fit(name, data=data, model=model)
fit.expression = 'line'
fit.independent = {'symbol': 't', 'name': 'Time', 'prefix': 'micro', 'units': 'µs'}
fit.dependent = {'name': 'Distance', 'prefix': 'kilo', 'units': 'km'}
fit.parameters = [
    {'symbol': 'v', 'guess': 1, 'prefix': 10**9, 'units': 'km/µs'},
    {'symbol': 'x_0', 'value': 1, 'prefix': 'kilo', 'units': 'km'},
]

# Save the fit to disk.
save_example_fit(fit)
