import json
import numpy
import scipy.optimize
import sympy

import scipy_data_fitting.core

class Fit:
    """
    Although not required at instantiation,
    `scipy_data_fitting.Fit.data` and `scipy_data_fitting.Fit.model`
    must be set to use most of this class.
    """

    def __init__(self, name=None, data=None, model=None):
        self.name = name
        """
        The identifier name for this object.
        """
        self.data = data
        """
        The `scipy_data_fitting.Data` instance to use for the fit.
        """
        self.model = model
        """
        The `scipy_data_fitting.Model` instance to use for the fit.
        """

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def description(self):
        """
        A short description for the fit.

        Will default to `scipy_data_fitting.Fit.name`.
        """
        if not hasattr(self, '_description'): return self.name
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def options(self):
        """
        Dictionary of options which affect the curve fitting algorithm.

        Must contain the key `fit_function` which must be set to
        the function that will perform the fit.

        The default options use `scipy.optimize.curve_fit`,
        and this class will assume any other specified function
        will receive the first four arguments in the same format as that
        and return an object of the same format that.

        All other options are passed as keyword arguments
        to the curve fitting function.

        Default:

            #!python
            {
                'fit_function': scipy.optimize.curve_fit,
                'maxfev': 1000,
            }
        """
        if not hasattr(self, '_options'):
            self._options = {
                'fit_function': scipy.optimize.curve_fit,
                'maxfev': 1000,
            }
        return self._options

    @options.setter
    def options(self, value):
        self._options = value

    @property
    def lambdify_options(self):
        """
        Dictionary of options which are passed as keyword arguments
        to `scipy_data_fitting.Model.lambdify`.

        Default:

            #!python
            {'modules': 'numpy'}
        """
        if not hasattr(self, '_lambdify_options'):
            self._lambdify_options = {
                'modules': 'numpy',
            }
        return self._lambdify_options

    @lambdify_options.setter
    def lambdify_options(self, value):
        self._lambdify_options = value

    @property
    def limits(self):
        """
        Limits to use for the independent variable whenever
        creating a line-space, plot, etc.

        Defaults to `(-x, x)` where `x` is the largest absolute value
        of the data corresponding to the independent variable.
        """
        if not hasattr(self, '_limits'):
            xmax = max(abs(self.data.array[0]))
            self._limits = (-xmax, xmax)

        return self._limits

    @limits.setter
    def limits(self, value):
        self._limits = value

    @property
    def expression(self):
        """
        The name of the expression to use for the fit
        as defined in `scipy_data_fitting.Model.expressions`.
        """
        return self._expression

    @expression.setter
    def expression(self, value):
        self._expression = value

    @property
    def replacements(self):
        """
        A single replacement or replacement group,
        or a list of replacements and replacement groups
        that will be applied to the expression
        defined by `scipy_data_fitting.Fit.expression`.

        See also `scipy_data_fitting.Model.replace`.

        This defaults to `None`.
        """
        if not hasattr(self, '_replacements'): self._replacements = None
        return self._replacements

    @replacements.setter
    def replacements(self, value):
        self._replacements = value

    @property
    def dependent(self):
        """
        A dictionary that defines the dependent variable.

        The only required key is `symbol`
        which defines the corresponding SymPy symbol.

        `symbol` may be given as a SymPy symbol or the name of a symbol
        defined in `scipy_data_fitting.Model.symbols`.

        If a `prefix` is given (as a number or string), it will affect the scale when
        creating a line-space, plot, etc.

        When `prefix` is given as a string, it will be converted to a number from [`scipy.constants`][1].

        `name` and `units` are only for display purposes.

        Other keys can be added freely and will be available
        as metadata for the various output formats.

        Defaults to `{}`.

        Example:

            #!python
            {'symbol': 'V', 'name': 'Voltage', 'prefix': 'kilo', 'units': 'kV'}

        [1]: http://docs.scipy.org/doc/scipy/reference/constants.html
        """
        if not hasattr(self, '_dependent'): self._dependent = {}
        return self._dependent

    @dependent.setter
    def dependent(self, value):
        self._dependent = value

    @property
    def independent(self):
        """
        A dictionary that defines the independent variable.

        This is not required, but the possible keys are the same as
        the optional ones explained in `scipy_data_fitting.Fit.independent`.

        This defaults to `{}`.

        Example:

            #!python
            {'name': 'Time', 'prefix': 'milli', 'units': 'ms'}
        """
        if not hasattr(self, '_independent'): self._independent = {}
        return self._independent

    @independent.setter
    def independent(self, value):
        self._independent = value

    @property
    def free_variables(self):
        """
        Free variables are useful when `scipy_data_fitting.Model.lambdify` is insufficient.

        Any free variables will correspond to the first arguments of
        `scipy_data_fitting.Fit.function`.

        Any free variables must be resolved before attempting any fitting (see example).

        This defaults to `[]`.

        Example:

            #!python
            >>> fit.independent = {'symbol': 'x'}
            >>> fit.parameters = [{'symbol': 'm', 'guess': 5}]
            >>> fit.free_variables = ['t']
            >>> f = fit.function # f(t, x, m)
            >>> fit.function = lambda *args: f(2, *args)
        """
        if not hasattr(self, '_free_variables'): self._free_variables = []
        return self._free_variables

    @free_variables.setter
    def free_variables(self, value):
        self._free_variables = value

    @property
    def quantities(self):
        """
        Quantities will be computed from an expression using the fitted parameters.

        The only required element in each dictionary is `expression`
        which can be a SymPy expression, or an expression name
        from `scipy_data_fitting.Model.expressions`.

        The expressions must not contain the symbols corresponding to
        `scipy_data_fitting.Fit.free_variables`, `scipy_data_fitting.Fit.independent`,
        or `scipy_data_fitting.Fit.dependent`.

        The other keys are the same as the optional ones explained
        in `scipy_data_fitting.Fit.independent`.

        This defaults to `[]`.

        Example:

            #!python
            [{'expression': 'tau', 'name': 'τ', 'prefix': 'milli', 'units': 'ms'}]
        """
        if not hasattr(self, '_quantities'): self._quantities = []
        return self._quantities

    @quantities.setter
    def quantities(self, value):
        self._quantities = value

    @property
    def constants(self):
        """
        Use constants to associate symbols in expressions with numerical values
        when not specifying them as fixed parameters.

        Each constant must contain the keys `symbol` and `value`.

        `symbol` may be given as a SymPy symbol or the name of a symbol
        defined in `scipy_data_fitting.Model.symbols`.

        If a `prefix` is specified, the value will be multiplied by it before being used.

        The value (also prefix) is either numerical,
        or a string which will be converted to a number from [`scipy.constants`][1].

        This defaults to `[]`.

        Example:

            #!python
            [
                {'symbol': 'c', 'value': 'c'},
                {'symbol': 'a', 'value': 'Bohr radius'},
                {'symbol': 'M', 'value': 2, 'prefix': 'kilo'},
            ]

        [1]: http://docs.scipy.org/doc/scipy/reference/constants.html
        """
        if not hasattr(self, '_constants'): self._constants = []
        return self._constants

    @constants.setter
    def constants(self, value):
        self._constants = value

    @property
    def parameters(self):
        """
        Each parameter is must contain the key `symbol`
        and a key which is either `value` or `guess`.

        `symbol` may be given as a SymPy symbol or the name of a symbol
        defined in `scipy_data_fitting.Model.symbols`.

        When a `guess` is given, that parameter is treated as a fitting parameter
        and the `guess` is used as a starting point.

        When `value` is given, the given value is fixed.

        If a `prefix` is specified, the `value` or `guess` will
        be multiplied by it before being used.

        When `prefix` is given as a string, it will be converted to a number from [`scipy.constants`][1].

        When appearing in metadata, values will be scaled back by the prefix.

        In the example below, the value for `L` used in computation will be `0.003`
        but when used for display, it will appear as `3 mm`.

        `name` and `units` are only for display purposes.

        Other keys can be added freely and will be available
        as metadata for the various output formats.

        Example:

            #!python
            [
                {'symbol': 'L', 'value': 3, 'prefix': 'milli', 'units': 'mm'},
                {'symbol': 'b', 'guess': 3, 'prefix': 'milli', 'units': 'mm'},
                {'symbol': 'm', 'guess': 3},
            ]

        [1]: http://docs.scipy.org/doc/scipy/reference/constants.html
        """
        if not hasattr(self, '_parameters'): self._parameters = []
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        self._parameters = value

    @property
    def fitting_parameters(self):
        """
        A list containing only elements of `scipy_data_fitting.Fit.parameters`
        which do not specify a `value` key.
        """
        return [ v for v in self.parameters if not 'value' in v ]

    @property
    def fixed_parameters(self):
        """
        A list containing only elements of `scipy_data_fitting.Fit.parameters`
        which do specify a `value` key.
        """
        return [ v for v in self.parameters if 'value' in v ]

    @property
    def expression(self):
        """
        The SymPy expression that will be used to generate
        the function that will be used for fitting.

        Any replacements defined in `scipy_data_fitting.Fit.replacements`
        are applied to the base expression before returning.

        This always returns a SymPy expression, but it may be set using a string,
        in which case the base expression will be looked up in `scipy_data_fitting.Model.expressions`.

        Example:

            #!python
            >>> fit.expression = 'line'
            >>> fit.expression # fit.model.expressions['line'] after replacements
        """
        return self.model.replace(self._expression, self.replacements)

    @expression.setter
    def expression(self, value):
        self._expression = value

    @property
    def all_variables(self):
        """
        A flat tuple of all symbols taken in order from the following:

        1. `scipy_data_fitting.Fit.free_variables`
        2. `scipy_data_fitting.Fit.independent`
        3. `scipy_data_fitting.Fit.fitting_parameters`
        4. `scipy_data_fitting.Fit.fixed_parameters`
        5. `scipy_data_fitting.Fit.constants`
        """
        variables = []
        variables.extend(self.free_variables)
        variables.append(self.independent['symbol'])
        variables.extend([ param['symbol'] for param in self.fitting_parameters ])
        variables.extend([ param['symbol'] for param in self.fixed_parameters ])
        variables.extend([ const['symbol'] for const in self.constants ])

        symbols = []
        for variable in variables:
            if isinstance(variable, str):
                symbols.append(self.model.symbol(variable))
            else:
                symbols.append(variable)

        return tuple(symbols)

    @property
    def fixed_values(self):
        """
        A flat tuple of all values corresponding to `scipy_data_fitting.Fit.fixed_parameters`
        and `scipy_data_fitting.Fit.constants` after applying any prefixes.

        The values mimic the order of those lists.
        """
        constant = scipy_data_fitting.core.get_constant
        prefix = scipy_data_fitting.core.prefix_factor

        values = []
        values.extend([ prefix(param) * param['value'] for param in self.fixed_parameters ])
        values.extend([ prefix(const) * constant(const['value']) for const in self.constants ])

        return tuple(values)

    @property
    def function(self):
        """
        The function used to perform the fit.

        Its number of arguments and their order is determined by items 1, 2, and 3
        as listed in `scipy_data_fitting.Fit.all_variables`.

        It is a functional form of `scipy_data_fitting.Fit.expression` converted
        using `scipy_data_fitting.Model.lambdify`.

        See also `scipy_data_fitting.Fit.lambdify_options`.

        Note that the function will be generated on each call unless this is set manually.

        All values passed to this function will be multiplied by their corresponding prefix.
        """
        if hasattr(self,'_function'): return self._function
        function = self.model.lambdify(self.expression, self.all_variables, **self.lambdify_options)
        return lambda *x: function(*(x + self.fixed_values))

    @function.setter
    def function(self, value):
        self._function = value

    @property
    def curve_fit(self):
        """
        Fits `scipy_data_fitting.Fit.function` to the data and returns
        the output from the specified curve fit function.

        See also `scipy_data_fitting.Fit.options`.
        """
        if not hasattr(self,'_curve_fit'):
            prefix = scipy_data_fitting.core.prefix_factor
            options = self.options.copy()
            fit_function = options.pop('fit_function')
            function = self.function
            independent_values = self.data.array[0]
            dependent_values = self.data.array[1]
            p0 = [ prefix(param) * param['guess'] for param in self.fitting_parameters ]

            self._curve_fit = fit_function(
                function, independent_values, dependent_values, p0, **options)

        return self._curve_fit

    @property
    def fitted_parameters(self):
        """
        A tuple of fitted values for the `scipy_data_fitting.Fit.fitting_parameters`.

        The values in this tuple are not scaled by the prefix,
        as they are passed back to `scipy_data_fitting.Fit.function`
        for `scipy_data_fitting.Fit.function`,
        e.g. in most standard use cases these would be the SI values.
        """
        if hasattr(self,'_fitted_parameters'): return self._fitted_parameters
        return tuple(self.curve_fit[0])

    @property
    def fitted_function(self):
        """
        A function of the single independent variable after
        partially evaluating `scipy_data_fitting.Fit.function` at
        the `scipy_data_fitting.Fit.fitted_parameters`.
        """
        function = self.function
        fitted_parameters = self.fitted_parameters
        return lambda x: function(x, *fitted_parameters)

    def clear_fit(self):
        """
        For performance, the results of the curve fit are saved in
        `scipy_data_fitting.Fit._curve_fit` and `scipy_data_fitting.Fit._fitted_parameters`.

        This clears these attributes.
        """
        del self._curve_fit
        del self._fitted_parameters

    @property
    def computed_quantities(self):
        """
        A list of the quantities defined in `scipy_data_fitting.Fit.quantities`
        evaluated with `scipy_data_fitting.Fit.fitted_parameters`.

        The list is identical to what is set with `scipy_data_fitting.Fit.quantities`
        but in each dictionary, the key `expression` is removed,
        and the key `value` is added with the value of the quantity.

        The quantity is computed using values multiplied by their prefix as in
        `scipy_data_fitting.Fit.function`. Once computed, the reported value is
        scaled by the inverse prefix.
        """
        return [ self.compute_quantity(quantity) for quantity in self.quantities ]

    def compute_quantity(self, quantity):
        """
        Processes a single quantity as described and used
        in `scipy_data_fitting.Fit.computed_quantities`.
        """
        quantity = quantity.copy()
        prefix = scipy_data_fitting.core.prefix_factor
        expression = self.model.replace(quantity.pop('expression'), self.replacements)
        variables = self.all_variables[len(self.free_variables) + 1:]
        function = self.model.lambdify(expression, variables, **self.lambdify_options)
        quantity['value'] = function(*(self.fitted_parameters + self.fixed_values)) * prefix(quantity)**(-1)
        return quantity

    @property
    def computed_fitting_parameters(self):
        """
        A list identical to what is set with `scipy_data_fitting.Fit.fitting_parameters`,
        but in each dictionary, the key `value` is added with the fitted value of the quantity.
        The reported value is scaled by the inverse prefix.
        """
        prefix = scipy_data_fitting.core.prefix_factor
        fitted_parameters = []
        for (i, v) in enumerate(self.fitting_parameters):
            param = v.copy()
            param['value'] = self.fitted_parameters[i] * prefix(param)**(-1)
            fitted_parameters.append(param)

        return fitted_parameters

    @property
    def metadata(self):
        """
        A dictionary which summarizes the results of the fit:

            #!python
            {
                'name': self.name,
                'description': self.description,
                'independent': self.independent,
                'dependent': self.dependent,
                'quantities': self.computed_quantities,
                'fixed_parameters': self.fixed_parameters,
                'fitted_parameters': self.computed_fitting_parameters,
            }
        """
        return {
          'name': self.name,
          'description': self.description,
          'independent': self.independent,
          'dependent': self.dependent,
          'quantities': self.computed_quantities,
          'fixed_parameters': self.fixed_parameters,
          'fitted_parameters': self.computed_fitting_parameters,
        }

    def pointspace(self, **kwargs):
        """
        Returns a dictionary with the keys `data` and `fit`.

        `data` is just `scipy_data_fitting.Data.array`.

        `fit` is a two row [`numpy.ndarray`][1], the first row values correspond
        to the independent variable and are generated using [`numpy.linspace`][2].
        The second row are the values of `scipy_data_fitting.Fit.fitted_function`
        evaluated on the linspace.

        For both `fit` and `data`, each row will be scaled by the corresponding
        inverse prefix if given in `scipy_data_fitting.Fit.independent`
        or `scipy_data_fitting.Fit.dependent`.

        Any keyword arguments are passed to [`numpy.linspace`][2].

        [1]: http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html
        [2]: http://docs.scipy.org/doc/numpy/reference/generated/numpy.linspace.html
        """
        prefix = scipy_data_fitting.core.prefix_factor
        scale_array = numpy.array([
            [prefix(self.independent)**(-1)],
            [prefix(self.dependent)**(-1)]
        ])

        linspace = numpy.linspace(self.limits[0], self.limits[1], **kwargs)
        return {
          'data': self.data.array * scale_array,
          'fit': numpy.array([linspace, self.fitted_function(linspace)]) * scale_array
        }

    def to_json(self, path, points=50):
        """
        Write the results of the fit to a json file at `path`.

        `points` will define the length of the `fit` array.

        The json object has the form

            #!text
            {
                'data': [ [x1, y1], [x2, y2], ... ],
                'fit': [ [x1, y1], [x2, y2], ... ],
                'meta': self.metadata
            }
        """
        pointspace = self.pointspace(num=points)
        fit_points = numpy.dstack(pointspace['fit'])[0]
        data_points = numpy.dstack(pointspace['data'])[0]

        fit = [ [ point[0],  point[1] ] for point in fit_points ]
        data = [ [ point[0],  point[1] ] for point in data_points ]

        f = open(path, 'w')
        json.dump({'data': data, 'fit': fit, 'meta': self.metadata}, f)
        f.close
