from scipy_data_fitting import Model

from nose.tools import *

class TestModel():

    def test_symbol(self):
        model = Model()
        model.add_symbol('x')
        eq_(model.symbol('x'), model.symbols['x'])

    def test_add_symbol(self):
        model = Model()
        model.add_symbol('x')
        model.add_symbol('why', string='y')
        eq_(len(model.symbols), 2)
        eq_(model.symbols['x'].name, 'x')
        eq_(model.symbols['why'].name, 'y')

    def test_add_symbols(self):
        model = Model()
        model.add_symbols('x', 'y', 'z')
        eq_(len(model.symbols), 3)
        eq_(model.symbols['x'].name, 'x')
        eq_(model.symbols['y'].name, 'y')

    def test_get_symbols(self):
        model = Model()
        model.add_symbols('x', 'y', 'z')
        x, y, z = model.get_symbols('x', 'y', 'z')
        eq_(x, model.symbols['x'])
        eq_(y, model.symbols['y'])

    def get_model(self):
        model = Model()
        model.test_symbols = ('x', 'y', 'z')
        model.add_symbols(*model.test_symbols)
        x, y, z = model.get_symbols(*model.test_symbols)
        model.expressions['exp'] = x + y
        model.replacements['rep_1'] = (x, y + z)
        model.replacements['rep_2'] = (z, x * x)
        model.replacements['rep_3'] = (x, y * z)
        model.replacement_groups['rep_g'] = ['rep_1', 'rep_2']
        return model

    def test_replace(self):
        model = self.get_model()
        x, y, z = model.get_symbols(*model.test_symbols)
        eq_(model.replace(x + y, (x, y + z)), y + z + y)

    def test_replace_with_empty_replacements(self):
        model = self.get_model()
        x, y, z = model.get_symbols(*model.test_symbols)
        eq_(model.replace(x + y, []), x + y)

    def test_replace_using_expressions(self):
        model = self.get_model()
        x, y, z = model.get_symbols(*model.test_symbols)
        eq_(model.replace('exp', (x, y + z)), y + z + y)
        eq_(model.replace('exp', [(x, y + z), (y, x)]), x + z + x)

    def test_replace_using_replacements(self):
        model = self.get_model()
        x, y, z = model.get_symbols(*model.test_symbols)
        eq_(model.replace('exp', 'rep_1'), y + z + y)
        eq_(model.replace('exp', ['rep_1', 'rep_2']), y + x * x + y)

    def test_replace_using_replacement_groups(self):
        model = self.get_model()
        x, y, z = model.get_symbols(*model.test_symbols)
        eq_(model.replace('exp', 'rep_g'), y + x * x + y)
        eq_(model.replace('exp', ['rep_g', 'rep_3']), y + y * z * y * z + y)

    def test_lambdify(self):
        model = self.get_model()
        x, y, z = model.get_symbols(*model.test_symbols)
        f = model.lambdify(x + y, (x, y))
        eq_(f(42, 10), 52)

    def test_lambdify_with_kwargs(self):
        model = self.get_model()
        x, y, z = model.get_symbols(*model.test_symbols)
        f = model.lambdify(x + y, (x, y), modules='numpy')
        eq_(f(42, 10), 52)

    def test_lambdify_with_expressions(self):
        model = self.get_model()
        x, y, z = model.get_symbols(*model.test_symbols)
        f = model.lambdify('exp', (x, y))
        eq_(f(42, 10), 52)

    def test_lambdify_with_symbols_as_strings(self):
        model = self.get_model()
        x, y, z = model.get_symbols(*model.test_symbols)
        f = model.lambdify('exp', (x, 'y'))
        eq_(f(42, 10), 52)

    def test_lambdify_with_one_symbol(self):
        model = self.get_model()
        x, y, z = model.get_symbols(*model.test_symbols)
        f = model.lambdify(x ** 2, x)
        eq_(f(3), 9)

    def test_lambdify_with_one_symbol_as_string(self):
        model = self.get_model()
        x, y, z = model.get_symbols(*model.test_symbols)
        f = model.lambdify(x ** 2, 'x')
        eq_(f(3), 9)
