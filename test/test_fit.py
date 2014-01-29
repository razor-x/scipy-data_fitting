from scipy_data_fitting import Data
from scipy_data_fitting import Model
from scipy_data_fitting import Fit

import numpy, sympy
from nose.tools import *
from numpy.testing import *

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

    def get_fit_for_fitting(self):
        fit = Fit('exponential_fit',
            data=self.get_data(),
            model=self.get_model())
        fit.expression = 'exp'
        fit.independent = {'symbol': 't'}
        fit.parameters = [
            {'symbol': 'a', 'guess': 10},
            {'symbol': 'k', 'guess': 20},
        ]
        return fit

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
        fit = Fit(model=self.get_model())
        expression = fit.model.expressions['exp']
        fit.expression = expression
        eq_(fit.expression, expression)

    def test_expression_with_string(self):
        fit = Fit(model=self.get_model())
        expression = fit.model.expressions['exp']
        fit.expression = 'exp'
        eq_(fit.expression, expression)

    def test_expression_with_replacements(self):
        fit = Fit(model=self.get_model())
        fit.replacements = 'tau'
        fit.expression = fit.model.expressions['exp']
        a, t, tau = fit.model.get_symbols('a', 't', 'τ')
        expression = a * sympy.functions.exp(-t / tau)
        eq_(fit.expression, expression)

    def test_expression_with_string_and_replacements(self):
        fit = Fit(model=self.get_model())
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

    def test_fixed_values(self):
        fit = Fit(model=Model())
        fit.parameters = [
            {'symbol': 'D', 'guess': 2},
            {'symbol': 'k', 'value': 3, 'prefix': 'kilo'},
            {'symbol': 'm', 'value': 4},
        ]
        fit.constants = [
            {'symbol': 'a', 'value': 10},
            {'symbol': 'b', 'value': 5, 'prefix': 'milli'},
            {'symbol': 'c', 'value': 'Avogadro constant'},
        ]
        eq_(fit.fixed_values, (3000, 4, 10, 0.005, 6.02214129e+23))

    def test_function(self):
        fit = self.get_fit_for_fitting()
        function = fit.function
        linspace = fit.data.array[0]
        values = fit.data.array[1]
        assert_almost_equal(function(linspace, 2, 3), values)

    def test_function_with_more_symbols(self):
        fit = Fit()
        fit.model = Model()
        symbols = ('x', 'a', 'b', 'c', 'd', 'e', 'f')
        fit.model.add_symbols(*symbols)
        x, a, b, c, d, e, f = fit.model.get_symbols(*symbols)
        fit.model.expressions['exp'] = a * f + b * e + x * c + d
        fit.expression = 'exp'
        fit.independent = {'symbol': 'x'}
        fit.parameters = [
            {'symbol': 'a', 'guess': 2},
            {'symbol': 'b', 'guess': 3},
            {'symbol': 'c', 'value': 4, 'prefix': 'kilo'},
            {'symbol': 'd', 'value': 5},
        ]
        fit.constants = [
            {'symbol': 'e', 'value': 10},
            {'symbol': 'f', 'value': 12, 'prefix': 'milli'},
        ]
        eq_(fit.function(2, 4, 7), 8075.048)

    def test_curve_fit(self):
        fit = self.get_fit_for_fitting()
        assert_almost_equal(fit.curve_fit[0], [2, 3])

    def test_fitting_paramters(self):
        fit = self.get_fit_for_fitting()
        assert_almost_equal(fit.fitted_parameters, (2, 3))

    def test_fitted_function(self):
        fit = self.get_fit_for_fitting()
        linspace = fit.data.array[0]
        values = fit.data.array[1]
        assert_almost_equal(fit.fitted_function(linspace), values)

    def test_computed_quantities(self):
        fit = self.get_fit_for_fitting()
        fit.model.expressions['k'] = fit.model.symbol('k')
        fit.replacements = 'tau'
        fit.parameters = [
            {'symbol': 'a', 'guess': 10},
            {'symbol': 'τ', 'guess': 0.3},
        ]
        fit.quantities = [
            {'expression': 'k', 'name': 'konstant'},
            {'expression': 'k', 'prefix': 'milli', 'units': 'mm'},
        ]
        computed_quantities = [
            {'value': 3.0, 'name': 'konstant'},
            {'value': 3000, 'prefix': 'milli', 'units': 'mm'},
        ]
        eq_(fit.computed_quantities, computed_quantities)

    def test_computed_fitting_parameters(self):
        fit = self.get_fit_for_fitting()
        fit.parameters = [
            {'symbol': 'a', 'guess': 10, 'prefix': 'kilo', 'units': 'km'},
            {'symbol': 'k', 'guess': 20},
        ]
        computed_fitting_parameters = [
            {'symbol': 'a', 'guess': 10, 'prefix': 'kilo', 'units': 'km', 'value': 0.002},
            {'symbol': 'k', 'guess': 20, 'value': 3},
        ]
        eq_(fit.computed_fitting_parameters, computed_fitting_parameters)

    def test_pointspace(self):
        fit = self.get_fit_for_fitting()
        pointspace = fit.pointspace()
        linspace = numpy.linspace(fit.limits[0], fit.limits[1])
        assert isinstance(pointspace['data'], numpy.ndarray)
        assert isinstance(pointspace['fit'], numpy.ndarray)
        assert_almost_equal(pointspace['data'], fit.data.array)
        assert_almost_equal(pointspace['fit'], [linspace, fit.fitted_function(linspace)])

    def test_pointspace_with_scale(self):
        fit = self.get_fit_for_fitting()
        fit.independent['prefix'] = 100
        fit.dependent['prefix'] = 2
        pointspace = fit.pointspace()
        linspace = numpy.linspace(fit.limits[0], fit.limits[1])
        assert_almost_equal(pointspace['data'], [fit.data.array[0] / 100, fit.data.array[1] / 2])
        assert_almost_equal(pointspace['fit'], [linspace / 100, fit.fitted_function(linspace) / 2])
