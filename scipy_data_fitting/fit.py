import json
import numpy
import scipy.constants
import scipy.optimize
import sympy

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
        if not hasattr(self, '_description'): self._description = self.name
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

        The default options use `scipy.optimize.curve_fit`
        and this class will assume any other specified function
        will return an object of the same format.

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

        This defaults to `[]`.
        """
        if not hasattr(self, '_replacements'): self._replacements = []
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

        When `prefix` is given as a string, it will be converted to a number
        from [SciPy constants](http://docs.scipy.org/doc/scipy/reference/constants.html).

        `name` and `units` are only for display purposes.

        Other keys can be added freely and will be available
        as metadata for the various output formats.

        Example:

            #!python
            {'symbol': 'V', 'name': 'Voltage', 'prefix': 'kilo', 'units': 'kV'}
        """
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
