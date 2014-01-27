from scipy_data_fitting import Data

import csv, os, tempfile
from nose.tools import *
from numpy.testing import *

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
        cls.data_files = [ cls.write_data(*args) for args in test_data_files ]

    @classmethod
    def teardown_class(cls):
        for data_file in cls.data_files:
            os.remove(data_file['filename'])

    @classmethod
    def write_data(cls, delimiter, headers):
        filename = tempfile.mkstemp(prefix='scipy_data_fitting_test_')[1]
        with open(filename, 'w+') as datafile:
            writer = csv.writer(datafile, delimiter=delimiter)
            if headers: writer.writerow(headers)
            writer.writerows(cls.raw_data_pairs)

        return {'delimiter': delimiter, 'headers': headers, 'filename': filename}

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
        assert_almost_equal(data.scale, (2, 6.02214129e+23))
