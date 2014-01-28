from scipy_data_fitting import Data
from scipy_data_fitting import Model
from scipy_data_fitting import Fit

import numpy
from nose.tools import *

class TestFit():

    def test_limits(self):
        data = Data()
        data.array = numpy.array([ [1, 2], [3, 4] ])
        fit = Fit(data=data)
        eq_(fit.limits, (-2, 2))
