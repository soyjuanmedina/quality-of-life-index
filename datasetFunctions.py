"""All the function used to manage dataset."""

from pyjstat import pyjstat
import json
import urllib.request as urllib2
from collections import OrderedDict


def getDatasetFromJsonUrlWLabel(jsonurl):
    """Recive a json url and return a dataset."""
    # Load the data from JSON. Important: JSON data must be retrieved in order;
    jsonurl_data = json.load(
        urllib2.urlopen(jsonurl),
        object_pairs_hook=OrderedDict)
    jsonurl_ddbb = pyjstat.from_json_stat(
        jsonurl_data)
    # Get the first result, since we're using only one input dataset
    jsonurl_dataset = jsonurl_ddbb[0]
    return jsonurl_dataset

def getDatasetFromJsonUrl(jsonurl):
    """Recive a json url and return a dataset."""
    # Load the data from JSON. Important: JSON data must be retrieved in order;
    jsonurl_data = json.load(
        urllib2.urlopen(jsonurl),
        object_pairs_hook=OrderedDict)
    jsonurl_ddbb = pyjstat.from_json_stat(
        jsonurl_data, naming="id")
    # Get the first result, since we're using only one input dataset
    jsonurl_dataset = jsonurl_ddbb[0]
    return jsonurl_dataset


def getDataForVariable(dataset, name, variable):
    """Recive a json url and return a dataset."""
    # Filter the year to plot
    dataset_filter_data = dataset[dataset[name] == variable]
    return dataset_filter_data

def getDataForIncludeVariable(dataset, name, variable):
    """Recive a json url and return a dataset."""
    # Filter the year to plot
    dataset_filter_data = dataset[dataset[name].str.contains(variable)]
    return dataset_filter_data


def chooseVariableInDataset(dataset, variable):
    """Recive a dataset and return the data of the variable."""
    # Get the last year we have data
    dataset_LastYear = list(dataset['Year'])[-1]
    # Filter the year to plot
    dataset_LastYear_data = dataset[dataset['Year'] == dataset_LastYear]
    return dataset_LastYear_data
