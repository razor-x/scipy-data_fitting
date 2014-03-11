import os
import sympy
from example_helper import save_example_fit
from scipy_data_fitting import Data, Model, Fit

#
# Example of a fit to a sine wave with error bars.
#

name = 'wave'

# Load data from a csv file.
data = Data(name)
data.path = os.path.join('examples','data', 'wave.csv')
data.genfromtxt_args['skip_header'] = 1
data.error = (0.1, 0.05)

# Create a wave model.
model = Model(name)
model.add_symbols('t', 'A', 'ω', 'δ')
A, t, ω, δ = model.get_symbols('A', 't', 'ω', 'δ')
model.expressions['wave'] = A * sympy.functions.sin(ω * t + δ)
model.expressions['frequency'] = ω / (2 * sympy.pi)

# Create the fit using the data and model.
fit = Fit(name, data=data, model=model)
fit.expression = 'wave'
fit.independent = {'symbol': 't', 'name': 'Time', 'units': 's'}
fit.dependent = {'name': 'Voltage', 'prefix': 'kilo', 'units': 'kV'}
fit.parameters = [
    {'symbol': 'A', 'value': 0.3, 'prefix': 'kilo', 'units': 'kV'},
    {'symbol': 'ω', 'guess': 1, 'units': 'Hz'},
    {'symbol': 'δ', 'guess': 1},
]
fit.quantities = [
    {'expression': 'frequency', 'name': 'Frequency', 'units': 'Hz'},
    {'expression': 1 / model.expressions['frequency'] , 'name': 'Period', 'units': 's'},
]

# Save the fit to disk.
save_example_fit(fit)
