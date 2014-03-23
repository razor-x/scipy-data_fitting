import matplotlib.pyplot

class Plot():
    """
    Use a `figure.Plot` object to create matplotlib plots
    from `figure.Fit` objects.

    Example:

        #!python
        >>> figure = Plot.new_figure()
        >>> fit = Fit(path='fit.json')
        >>> plot = Plot(fit=fit, plt=figure.add_subplot(111))
        >>> plot.plot_data()
        >>> plot.plot_fit()
        >>> figure.savefig(figure.svg)
        >>> Plot.close_figure(figure)
    """

    def __init__(self, fit=None, plt=None):
        self.fit = fit
        """
        The `figure.Fit` object to associate with this plot.
        """

        self.plt = plt
        """
        The matplotlib subplot associated with this plot.

        Assign the object returned by [`matplotlib.figure.Figure.add_subplot`][1] to this property.

        [1]: http://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure.add_subplot
        """

    @property
    def fit(self):
        return self._fit

    @fit.setter
    def fit(self, value):
        self._fit = value

    @property
    def plt(self):
        return self._plt

    @plt.setter
    def plt(self, value):
        self._plt = value

    @property
    def options(self):
        """
        Dictionary of options which affect the plot style.

        Must contain the keys `data` and `fit` whose values are dictionaries.

        Options given in `data` and `fit` are passed as keyword arguments
        to [`matplotlib.pyplot.plot`][1] for the corresponding plot.

        Default:

            #!python
            {
                'data': {'marker': '.', 'linestyle': 'None'},
                'fit': {},
            }

        [1]: http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.plot
        """
        if not hasattr(self, '_options'):
            self._options = {
                'data': {'marker': '.', 'linestyle': 'None'},
                'fit': {},
            }
        return self._options

    @options.setter
    def options(self, value):
        self._options = value

    def plot_data(self):
        """
        Add the data points to the plot.
        """
        self.plt.plot(*self.fit.data, **self.options['data'])

    def plot_fit(self):
        """
        Add the fit to the plot.
        """
        self.plt.plot(*self.fit.fit, **self.options['fit'])

    def add_xlabel(self, text=None):
        """
        Add a label to the x-axis.
        """
        x = self.fit.meta['independent']
        if not text:
            text = '$' + x['tex_symbol'] + r'$ $(\si{' + x['siunitx'] +  r'})$'
        self.plt.set_xlabel(text)

    def add_ylabel(self, text=None):
        """
        Add a label to the y-axis.
        """
        y = self.fit.meta['dependent']
        if not text:
            text = '$' + y['tex_symbol'] + r'$ $(\si{' + y['siunitx'] +  r'})$'
        self.plt.set_ylabel(text)

    def add_text_table(self, rows, r0, dr, **kwargs):
        """
        Add text to a plot in a grid fashion.
        """
        for m, row in enumerate(rows):
            for n, column in enumerate(row):
                self.plt.text(r0[0] + dr[0] * n, r0[1] + dr[1] * m, column,
                    transform=self.plt.axes.transAxes, **kwargs)

    @staticmethod
    def new_figure(**kwargs):
        """
        Returns a new [`matplotlib.figure.Figure`][1] object.
        Keyword arguments are passed to [`matplotlib.pyplot.figure`][2].

        [1]: http://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure
        [2]: http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.figure
        """
        return matplotlib.pyplot.figure(**kwargs)

    @staticmethod
    def close_figure(figure):
        """
        Closes a [`matplotlib.figure.Figure`][1] object
        with [`matplotlib.pyplot.close`][2].

        [1]: http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.close
        """
        return matplotlib.pyplot.close(figure)

    @staticmethod
    def parameter_table(parameters):
        """
        Create
        """
        if not isinstance(parameters, list): parameters = [parameters]
        rows = []
        for param in parameters:
            row = []
            row.append('$' + param['tex_symbol'] + '$')
            row.append('$=$')
            row.append(r'$\SI{' + param['disply_value'] + '}{' + param['siunitx'] + '}$')
            rows.append(row)
        return rows
