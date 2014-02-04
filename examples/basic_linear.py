import os
from example_helper import save_example_fit
from scipy_data_fitting import Data, Model, Fit

#
# Example of a basic linear fit.
#

name = 'basic_linear'

# Load data from a csv file.
data = Data(name)
data.path = os.path.join('examples','data', 'linear.csv')

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
    {'symbol': 'x_0', 'value': 1, 'units': 'm'},
    {'symbol': 'v', 'guess': 1, 'units': 'm/s'},
]

# Save the fit to disk.
save_example_fit(fit)
