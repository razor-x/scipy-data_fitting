import json
import os
import shutil
from scipy_data_fitting import Plot

def save_example_fit(fit):
    """
    Save fit result to a json file and a plot to an svg file.
    """
    json_directory = os.path.join('examples', 'json')
    plot_directory = os.path.join('examples', 'plots')
    if not os.path.isdir(json_directory): os.makedirs(json_directory)
    if not os.path.isdir(plot_directory): os.makedirs(plot_directory)

    fit.to_json(os.path.join(json_directory, fit.name + '.json'), meta=fit.metadata)

    plot = Plot(fit)
    plot.save(os.path.join(plot_directory, fit.name + '.svg'))
    plot.close()

def reset_directory(directory):
    """
    Remove `directory` if it exists, then create it if it doesn't exist.
    """
    if os.path.isdir(directory): shutil.rmtree(directory)
    if not os.path.isdir(directory): os.makedirs(directory)
