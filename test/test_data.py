import csv
import numpy
import os
import tempfile

from nose.tools import *
from numpy.testing import *

from scipy_data_fitting import Data

class TestData():

    @classmethod
    def setup_class(cls):
        cls.raw_data = [
            [1, 3, 8, 5],
            [0, 2, 4, 7]
        ]
        cls.raw_data_pairs = list(zip(*cls.raw_data))

        test_data_files = [
            (',', []),
            (',', ['x', 'y']),
            ("\t", []),
            ("\t", ['r', 't']),
        ]
        cls.data_files = [ cls.write_data(cls.raw_data_pairs, *args) for args in test_data_files ]

        cls.error = [
            [0.1, 0.4, 0.6],
            [0.2, 0.5, 0.9],
            [0.3, 0.7, 1.1],
            [0.8, 1.2, 1.5]
        ]
        cls.error_pairs = list(zip(*cls.error))
        cls.error_file = cls.write_data(cls.error_pairs, ',', [])

    @classmethod
    def teardown_class(cls):
        for data_file in cls.data_files:
            os.remove(data_file['filename'])
        os.remove(cls.error_file['filename'])

    @classmethod
    def write_data(cls, data, delimiter, headers):
        filename = tempfile.mkstemp(prefix='scipy_data_fitting_test_')[1]
        with open(filename, 'w+') as datafile:
            writer = csv.writer(datafile, delimiter=delimiter)
            if headers: writer.writerow(headers)
            writer.writerows(data)

        return {'delimiter': delimiter, 'headers': headers, 'filename': filename}

    def test_scale_with_numbers_gives_numbers(self):
        data = Data()
        data.scale = (1, 2)
        eq_(data.scale, (1, 2))

    def test_scale_with_strings_gives_numbers(self):
        data = Data()
        data.scale = ('kilo', 'milli')
        assert_almost_equal(data.scale, (1000, 0.001))

    def test_scale_with_mixed_gives_numbers(self):
        data = Data()
        data.scale = (2, 'Avogadro constant')
        assert_array_almost_equal(data.scale, (2, 6.022140857e+23))

    def test_load_data(self):
        for data_file in self.data_files:
            data = Data()
            data.path = data_file['filename']
            data.genfromtxt_args['delimiter'] = data_file['delimiter']
            if data_file['headers']: data.genfromtxt_args['skip_header'] = 1
            yield assert_allclose, data.load_data(), self.raw_data

    def test_load_data_with_scale(self):
        data_file = self.data_files[0]
        data = Data()
        data.path = data_file['filename']
        data.genfromtxt_args['delimiter'] = data_file['delimiter']
        data.scale = (2, 5)

        raw_data_scaled = [
            [ 2 * x for x in self.raw_data[0] ],
            [ 5 * x for x in self.raw_data[1] ],
        ]
        assert_allclose(data.load_data(), raw_data_scaled)

    def test_error_makes_ndarray(self):
        data = Data()
        data.error = (0.1, None)
        assert_allclose(data.error[0], numpy.array(0.1))
        eq_(data.error[1], None)

        data.error = ([0.1, 0.2], None)
        assert_allclose(data.error[0], numpy.array([0.1, 0.2]))
        eq_(data.error[1], None)

        data.error = (0.1, 0.2)
        assert_allclose(data.error[0], numpy.array(0.1))
        assert_allclose(data.error[1], numpy.array(0.2))

        data.error = (0.1, [0.1, 0.2])
        assert_allclose(data.error[0], numpy.array(0.1))
        assert_allclose(data.error[1], numpy.array([0.1, 0.2]))

    def test_load_error(self):
        raw_error = numpy.array(self.error)
        data = Data()
        data.path = self.error_file['filename']

        data.error_columns = (1, None)
        assert_allclose(data.error[0], raw_error[1])
        eq_(data.error[1], None)

        del data._error
        data.error_columns = (None, 1)
        eq_(data.error[0], None)
        assert_allclose(data.error[1], raw_error[1])

        del data._error
        data.error_columns = (2, 1)
        assert_allclose(data.error[0], raw_error[2])
        assert_allclose(data.error[1], raw_error[1])

        del data._error
        data.error_columns = ((1, 2), None)
        assert_allclose(data.error[0], numpy.array([raw_error[1], raw_error[2]]))
        eq_(data.error[1], None)

        del data._error
        data.error_columns = (None, (1, 2))
        eq_(data.error[0], None)
        assert_allclose(data.error[1], numpy.array([raw_error[1], raw_error[2]]))

        del data._error
        data.error_columns = ((1, 2), 0)
        assert_allclose(data.error[0], numpy.array([raw_error[1], raw_error[2]]))
        assert_allclose(data.error[1], raw_error[0])

        del data._error
        data.error_columns = (0, (2, 1))
        assert_allclose(data.error[0], raw_error[0])
        assert_allclose(data.error[1], numpy.array([raw_error[2], raw_error[1]]))

        del data._error
        data.error_columns = ((1, 3), (0, 2))
        assert_allclose(data.error[0], numpy.array([raw_error[1], raw_error[3]]))
        assert_allclose(data.error[1], numpy.array([raw_error[0], raw_error[2]]))

    def test_load_error_with_scale(self):
        raw_error = numpy.array(self.error)
        data = Data()
        data.path = self.error_file['filename']
        data.scale = (2, 10)

        data.error_columns = ((1, 2), 0)
        assert_allclose(data.error[0], 2 * numpy.array([raw_error[1], raw_error[2]]))
        assert_allclose(data.error[1], 10 * raw_error[0])

        del data._error
        data.error_columns = (0, (2, 1))
        assert_allclose(data.error[0], 2 * raw_error[0])
        assert_allclose(data.error[1], 10 * numpy.array([raw_error[2], raw_error[1]]))

        del data._error
        data.error_columns = ((1, 3), (0, 2))
        assert_allclose(data.error[0], 2 * numpy.array([raw_error[1], raw_error[3]]))
        assert_allclose(data.error[1], 10 * numpy.array([raw_error[0], raw_error[2]]))
