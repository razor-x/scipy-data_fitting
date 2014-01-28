import scipy.constants

def get_constant(value):
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
