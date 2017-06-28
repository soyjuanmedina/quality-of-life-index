"""This script generate an index of quality of life from diferent index."""

import math
import pandas as pd
import numpy as np
from functions import asingNumberToTerritories, getCountieFromCode, asingNumbersToTerritories, diferenceToBest
from getIndexFunctions import getpurchasingPowerInclRentIndex, gethousepriceToIncomeRatioIndex, getsafetyIndex, gethealthIndex, getIndexbyPopulationIntoLimits
from datasetFunctions import getDatasetFromJsonUrl, getDataForVariable, getDatasetFromJsonUrlWLabel, getDataForIncludeVariable

from pyjstat import pyjstat
import json
import urllib.request as urllib2
from collections import OrderedDict

# Define the territories
COUNTIES = [
    'Carlow', 'Cavan', 'Clare', 'Cork', 'Donegal', 'Dublin', 'Galway', 'Kerry', 'Kildare',
    'Kilkenny', 'Laois', 'Leitrim', 'Limerick', 'Longford', 'Louth', 'Mayo', 'Meath', 'Monaghan',
    'Offaly', 'Roscommon', 'Sligo', 'Tipperary', 'Waterford', 'Westmeath', 'Wexford', 'Wicklow']

# ----------OBTAIN POPULATION ------------

# URL of the dataset for popullation
population_url = \
    'http://www.cso.ie/StatbankServices/StatbankServices.svc/jsonservice/responseinstance/CD101'

# Build the Dataset from JsonUrl
population_dataset = getDatasetFromJsonUrlWLabel(population_url)

# Get the last year we have data
dataset_LastYear = list(population_dataset['Census Year'])[-1]

# Filter the database for year
population_data = \
    getDataForVariable(population_dataset, 'Census Year', dataset_LastYear)

# Filter the database for other variables
population_dataYearSex = \
    getDataForVariable(population_data, 'Sex', 'Both sexes')
population_dataYearSexTown = \
    getDataForVariable(population_dataYearSex, 'Aggregate Town or Rural Area', 'State')
population_dataYearSexTownStatistic = \
    getDataForVariable(population_dataYearSexTown, 'Statistic', 'Population (Number)')

# Extractig the data
populationAllCounties = {}
for data in population_dataYearSexTownStatistic.iterrows():
    populationAllCounties[list(list(data)[1])[2]] = list(list(data)[1])[5]

# Sum population for Tipperary
populationAllCounties['Tipperary'] = populationAllCounties['South Tipperary']\
    + populationAllCounties['North Tipperary']

# Taking only data we need
population = asingNumbersToTerritories(COUNTIES, populationAllCounties)

# ----------FINISH POPULATION ------------


# ----------------------------OBTAIN HEALTH INDEX -------------------------------------------

# ----------OBTAIN healthCareExpenditure ------------

# URL of the dataset for healthCareExpenditure
healthCareExpenditure_url = \
    'http://www.cso.ie/StatbankServices/StatbankServices.svc/jsonservice/responseinstance/SHA07'

# Build the Dataset from JsonUrl
healthCareExpenditure_dataset = getDatasetFromJsonUrl(healthCareExpenditure_url)

# Get the last year we have data
dataset_LastYear = list(healthCareExpenditure_dataset['Year'])[-1]
healthCareExpenditure_data = \
    getDataForVariable(healthCareExpenditure_dataset, 'Year', dataset_LastYear)

# Extractig the data
healthCareExpenditureForYear = list(healthCareExpenditure_data['value'])[0]

# Calculate the data for each countie
healthCareExpenditureForCountie = (healthCareExpenditureForYear * 1000000) / len(COUNTIES)

# Given data for each countie
healthCareExpenditure = asingNumberToTerritories(COUNTIES, healthCareExpenditureForCountie)

# ----------FINISH healthCareExpenditure ------------

# Calculation logshealthIndex
logshealthIndex = {}
for territory in COUNTIES:
    logshealthIndex[territory] = math.log(healthCareExpenditure[territory] / population[territory])

# Obtain Constants from a file

with open("externaldata/linearcorrelationhealthIndex.txt") as f:
    linearcorrelationhealthIndex = dict(x.rstrip().split(':', 1) for x in f)

# Building the final healthIndex
average = float(linearcorrelationhealthIndex['Average'])
constant = float(linearcorrelationhealthIndex['Constant'])
healthIndex = {}
for territory in COUNTIES:
    healthIndex[territory] = logshealthIndex[territory] * average + constant

# ----------------------------FINISH HEALTH INDEX----------------------------------------------

print(healthIndex)
