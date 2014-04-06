import os
import json
import sympy

from example_helper import reset_directory
from scipy_data_fitting import Data, Model, Fit

#
# Create a linear fit and a wave fit,
# then save the results to json for display in fitalyzer.
#

class LinearData(Data):
    def __init__(self):
        self.path = os.path.join('examples', 'data', 'linear.csv')
        self.genfromtxt_args['skip_header'] = 1

class LinearModel(Model):
    def __init__(self):
        self.add_symbols('t', 'v', 'x_0')
        t, v, x_0 = self.get_symbols('t', 'v', 'x_0')
        self.expressions['line'] = v * t + x_0

class LinearFit(Fit):
    def __init__(self):
        self.name = 'linear'
        self.description = 'Linear fit example'
        self.data = LinearData()
        self.model = LinearModel()
        self.expression = 'line'
        self.independent = {'symbol': 't', 'name': 'Time', 'units': 's'}
        self.dependent = {'name': 'Distance', 'units': 'm'}
        self.parameters = [
            {'symbol': 'v', 'guess': 1, 'units': 'm/s'},
            {'symbol': 'x_0', 'value': 1, 'units': 'm'},
        ]

class WaveData(Data):
    def __init__(self):
        self.path = os.path.join('examples', 'data', 'wave.csv')
        self.genfromtxt_args['skip_header'] = 1

class WaveModel(Model):
    def __init__(self):
        self.add_symbols('t', 'A', 'ω', 'δ')
        A, t, ω, δ = self.get_symbols('A', 't', 'ω', 'δ')
        self.expressions['wave'] = A * sympy.functions.sin(ω * t + δ)
        self.expressions['frequency'] = ω / (2 * sympy.pi)

class WaveFit(Fit):
    def __init__(self):
        self.name = 'wave'
        self.description = 'Sine wave example'
        self.data = WaveData()
        self.model = WaveModel()
        self.expression = 'wave'
        self.independent = {'symbol': 't', 'name': 'Time', 'units': 's'}
        self.dependent = {'name': 'Voltage', 'prefix': 'kilo', 'units': 'kV'}
        self.parameters = [
            {'symbol': 'A', 'value': 0.3, 'prefix': 'kilo', 'units': 'kV'},
            {'symbol': 'ω', 'guess': 1, 'units': 'Hz'},
            {'symbol': 'δ', 'guess': 1},
        ]
        self.quantities = [
            {'expression': 'frequency', 'name': 'Frequency', 'units': 'Hz'},
            {'expression': 1 / self.model.expressions['frequency'] , 'name': 'Period', 'units': 's'},
        ]

json_directory = os.path.join('examples', 'fitalyzer')
reset_directory(json_directory)

fits = [LinearFit(), WaveFit()]
fit_metadata = []
for fit in fits:
    fit.to_json(os.path.join(json_directory, fit.name + '.json'))
    fit_metadata.append(fit.metadata)

f = open(os.path.join(json_directory, 'fits.json'), 'w')
json.dump(fit_metadata, f)
f.close
