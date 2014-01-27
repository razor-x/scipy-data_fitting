import numpy
import scipy.constants

class Data:
    """
    Provides an interface to load data from files into
    `numpy.Array` objects.

    Example:

        #!python
        >>> data = Data()
        >>> data.path = 'path/to/data.csv'
        >>> data.scale = (1, 'kilo')
        >>> data.array
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
        Data as a `numpy.Array` in the form

            #!python
            [
                [ x1, x2, x3, ... ],
                [ y1, y2, y3, ...]
            ]

        The x and y values will be scaled according to `scipy_data_fitting.Data.scale`.
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
        and converted to the corresponding number using `scipy.constants`.
        """
        if not hasattr(self, '_scale'): self._scale = (1, 1)
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = tuple( self.get_scale(v) for v in value )

    @property
    def genfromtxt_args(self):
        """
        Passed as keyword arguments to `numpy.genfromtxt`
        when called by `scipy_data_fitting.Data.load_data`.

        Default:

            #!python
            {
                'unpack': True,
                'delimiter': ',',
                'usecols': (0 ,1),
            }
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
        Loads data from `scipy_data_fitting.Data.path` using `numpy.genfromtxt`
        and returns a `numpy.Array`.

        Data is scaled according to `scipy_data_fitting.Data.scale`.
        """
        array = numpy.genfromtxt(self.path, **self.genfromtxt_args)

        if self.scale == (1, 1):
            return array
        else:
            return numpy.array([
                array[0] * self.scale[0],
                array[1] * self.scale[1]
            ])

    @staticmethod
    def get_scale(value):
        """
        When `value` is a string, get the corresponding constant
        from `scipy.constants`.
        """
        if type(value) is str:
            if hasattr(scipy.constants, value):
                return getattr(scipy.constants, value)
            else:
                return scipy.constants.physical_constants[value][0]
        else:
            return value
