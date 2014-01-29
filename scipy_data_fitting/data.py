import numpy

import scipy_data_fitting.core

class Data:
    """
    Provides an interface to load data from files into
    [`numpy.ndarray`][1] objects.

    Example:

        #!python
        >>> data = Data()
        >>> data.path = 'path/to/data.csv'
        >>> data.scale = (1, 'kilo')
        >>> data.array

    [1]: http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html
    """

    def __init__(self, name=None):
        self.name = name
        """
        The identifier name for this object.
        """

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def path(self):
        """
        Path to the file containing data to load.
        """
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def array(self):
        """
        Data as a [`numpy.ndarray`][1] in the form

            #!python
            [
                [ x1, x2, x3, ... ],
                [ y1, y2, y3, ...]
            ]

        The x and y values will be scaled according to `scipy_data_fitting.Data.scale`.

        [1]: http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html
        """
        if not hasattr(self, '_array'): self._array = self.load_data()
        return self._array

    @array.setter
    def array(self, value):
        self._array = value

    @property
    def scale(self):
        """
        Tuple `(x_scale, y_scale)` that defines how to scale data
        imported by `scipy_data_fitting.Data.load_data`.

        Data is imported, then values are multiplied by the corresponding
        scale value before retuning the array.

        If a scale is specified as a string,
        it will treated as a named physical constant
        and converted to the corresponding number using [`scipy.constants`][1].

        [1]: http://docs.scipy.org/doc/scipy/reference/constants.html
        """
        if not hasattr(self, '_scale'): self._scale = (1, 1)
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = tuple( scipy_data_fitting.core.get_constant(v) for v in value )

    @property
    def genfromtxt_args(self):
        """
        Passed as keyword arguments to [`numpy.genfromtxt`][1]
        when called by `scipy_data_fitting.Data.load_data`.

        Default:

            #!python
            {
                'unpack': True,
                'delimiter': ',',
                'usecols': (0 ,1),
            }

        [1]: http://docs.scipy.org/doc/numpy/reference/generated/numpy.genfromtxt.html
        """
        if not hasattr(self, '_genfromtxt_args'):
            self._genfromtxt_args = {
                'unpack': True,
                'delimiter': ',',
                'usecols': (0 ,1),
            }
        return self._genfromtxt_args

    @genfromtxt_args.setter
    def genfromtxt_args(self, value):
        self._genfromtxt_args = value

    def load_data(self):
        """
        Loads data from `scipy_data_fitting.Data.path` using [`numpy.genfromtxt`][1]
        and returns a [`numpy.ndarray`][2].

        Data is scaled according to `scipy_data_fitting.Data.scale`.

        [1]: http://docs.scipy.org/doc/numpy/reference/generated/numpy.genfromtxt.html
        [2]: http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html
        """
        array = numpy.genfromtxt(self.path, **self.genfromtxt_args)

        if self.scale == (1, 1):
            return array
        else:
            return numpy.array([
                array[0] * self.scale[0],
                array[1] * self.scale[1]
            ])
