from scipy_data_fitting import Data
from scipy_data_fitting import Model
from scipy_data_fitting import Fit

import numpy, sympy
from nose.tools import *

class TestFit():

    def get_model(self):
        model = Model('exponential_model')
        symbols = ('f', 'a', 'k', 't', 'τ')
        model.add_symbols(*symbols)
        f, a, k, t, tau = model.get_symbols(*symbols)
        model.expressions['f'] = f
        model.expressions['exp'] = a * sympy.functions.exp(- k * t)
        model.replacements['exp'] = (f, model.expressions['exp'])
        model.replacements['tau'] = (k, tau**(-1) )
        model.replacement_groups['all'] = ['exp', 'tau']
        return model

    def get_data(self):
        data = Data('exponential_data')
        model = self.get_model()
        function = model.lambdify('exp', ('t', 'a', 'k'), modules='numpy')
        linspace = numpy.linspace(-1, 1, 300, endpoint=True)
        data.array = numpy.array([ linspace, function(linspace, 2, 3) ])
        return data

    def get_fit(self):
        return Fit('exponential_fit',
            data=self.get_data(),
            model=self.get_model())

    def get_parameters(self):
        return [
            {'symbol': 'a', 'value': 2},
            {'symbol': 'b', 'value': 5},
            {'symbol': 'k', 'guess': 10},
            {'symbol': 'm', 'guess': 20},
        ]

    def test_limits(self):
        data = Data()
        data.array = numpy.array([ [1, 2], [3, 4] ])
        fit = Fit(data=data)
        eq_(fit.limits, (-2, 2))

    def test_fitting_parameters(self):
        fit = Fit()
        fit.parameters = self.get_parameters()
        eq_(fit.fitting_parameters, [{'symbol': 'k', 'guess': 10}, {'symbol': 'm', 'guess': 20}])

    def test_fixed_parameters(self):
        fit = Fit()
        fit.parameters = self.get_parameters()
        eq_(fit.fixed_parameters, [{'symbol': 'a', 'value': 2}, {'symbol': 'b', 'value': 5}])

    def test_expression(self):
        fit = self.get_fit()
        expression = fit.model.expressions['exp']
        fit.expression = expression
        eq_(fit.expression, expression)

    def test_expression_with_string(self):
        fit = self.get_fit()
        expression = fit.model.expressions['exp']
        fit.expression = 'exp'
        eq_(fit.expression, expression)

    def test_expression_with_replacements(self):
        fit = self.get_fit()
        fit.replacements = 'tau'
        fit.expression = fit.model.expressions['exp']
        a, t, tau = fit.model.get_symbols('a', 't', 'τ')
        expression = a * sympy.functions.exp(-t / tau)
        eq_(fit.expression, expression)

    def test_expression_with_string_and_replacements(self):
        fit = self.get_fit()
        fit.expression = 'exp'
        a, k, t, tau = fit.model.get_symbols('a', 'k', 't', 'τ')
        fit.replacements = (k, 1 / tau)
        expression = a * sympy.functions.exp(-t / tau)
        eq_(fit.expression, expression)

    def test_all_variables(self):
        fit = Fit(model=Model())
        symbols = ('t', 'u', 'x', 'm', 'D', 'k', 'τ', 'a', 'b')
        fit.model.add_symbols(*symbols)
        fit.free_variables = ['t', 'u']
        fit.independent = {'symbol': 'x'}
        fit.parameters = [
            {'symbol': 'm', 'guess': 2},
            {'symbol': 'D', 'guess': 2},
            {'symbol': fit.model.symbol('k'), 'value': 3},
            {'symbol': 'τ', 'value': 4},
        ]
        fit.constants = [
            {'symbol': 'a'},
            {'symbol': 'b'},
        ]
        eq_(fit.all_variables, tuple( fit.model.symbol(s) for s in symbols ))
