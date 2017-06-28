"""This script generate an index of quality of life from diferent index."""

import math
import numpy as np
import json
import urllib.request as urllib2
from functions import asingNumberToTerritories, getCountieFromCode, asingNumbersToTerritories, diferenceToBest
from getIndexFunctions import getpurchasingPowerInclRentIndex, gethousepriceToIncomeRatioIndex, madeQualityOfLifeIndex
from datasetFunctions import getDatasetFromJsonUrl, getDataForVariable, getDatasetFromJsonUrlWLabel, getDataForIncludeVariable

# Define the territories
COUNTIES = [
    'Carlow', 'Cavan', 'Clare', 'Cork', 'Donegal', 'Dublin', 'Galway', 'Kerry', 'Kildare',
    'Kilkenny', 'Laois', 'Leitrim', 'Limerick', 'Longford', 'Louth', 'Mayo', 'Meath', 'Monaghan',
    'Offaly', 'Roscommon', 'Sligo', 'Tipperary', 'Waterford', 'Westmeath', 'Wexford', 'Wicklow']

# ----------------------------CALCULATING PURCHASING POWER----------------------------
# URL of the dataset for purchasingPowerInclRentIndex
purchasingPowerInclRentIndex_url = \
    'http://www.cso.ie/StatbankServices/StatbankServices.svc/jsonservice/responseinstance/CPA05'

# Build the Dataset from JsonUrl
purchasingPowerInclRentIndex_dataset = getDatasetFromJsonUrl(purchasingPowerInclRentIndex_url)

# Get the last year we have data
dataset_LastYear = list(purchasingPowerInclRentIndex_dataset['Year'])[-1]
purchasingPowerInclRentIndex_data = \
    getDataForVariable(purchasingPowerInclRentIndex_dataset, 'Year', dataset_LastYear)

# Extractig the data
purchasingPowerInclRentIndexForYear = list(purchasingPowerInclRentIndex_data['value'])[0]

# Asing the data to each Countie
purchasingPowerCounties = asingNumberToTerritories(COUNTIES, purchasingPowerInclRentIndexForYear)

# Calculate the purchasingPowerInclRentIndex
purchasingPowerInclRentIndex = getpurchasingPowerInclRentIndex(purchasingPowerCounties)

# ----------------------------FINISH CALCULATING PURCHASING POWER----------------------------

# ----------------------------CALCULATING HOUSE PRICE TO INCOME RATIO----------------------------

# ---------GET HOUSE PRICE --------------
# URL of the dataset for houseprice
housePrice_url = \
    'http://www.cso.ie/StatbankServices/StatbankServices.svc/jsonservice/responseinstance/HSA06'

# Build the Dataset from JsonUrl
housePrice_dataset = getDatasetFromJsonUrl(housePrice_url)

# Get the last year we have data
dataset_LastYear = list(housePrice_dataset['Year'])[-1]

# Get data for the last year we have data
housePrice_data = \
    getDataForVariable(housePrice_dataset, 'Year', dataset_LastYear)

# Getting the areas
housePriceArea = list(housePrice_dataset['Area'])
areas = {}
for area in housePriceArea:
    areas[area] = area

# Filter the area to plot
housePrice_databyArea = {}
for area in areas:
    data = getDataForVariable(housePrice_data, 'Area', area).values
    average = (data[0][3] + data[1][3]) / 2
    con = getCountieFromCode(area)
    housePrice_databyArea[con] = average

# Asing data to each Countie and storage it
housePriceCounties = asingNumbersToTerritories(COUNTIES, housePrice_databyArea)

# ---------FINISH GET HOUSE PRICE --------------

# ---------GET AVERAGE EARNINGS --------------
# URL of the dataset for housepriceToIncomeRatio
averageEarnings_url = \
    'http://www.cso.ie/StatbankServices/StatbankServices.svc/jsonservice/responseinstance/EHA05'

# Build the Dataset from JsonUrl
averageEarnings_dataset = getDatasetFromJsonUrl(averageEarnings_url)

# Get the last year we have data
dataset_LastYear = list(averageEarnings_dataset['Year'])[-1]

# Get data for the variables we need
averageEarnings_dataYear = \
    getDataForVariable(averageEarnings_dataset, 'Year', dataset_LastYear)
averageEarnings_dataYearNace = \
    getDataForVariable(averageEarnings_dataYear, 'NACE Rev 2 Economic Sector', '-')
averageEarnings_dataYearNaceType = \
    getDataForVariable(averageEarnings_dataYearNace, 'Type of Employment', '-')
averageEarnings_data = getDataForVariable(averageEarnings_dataYearNaceType, 'Statistic', 'EHA05C05')

# Extractig the data
averageEarnings = list(averageEarnings_data['value'])[0]

# Asing the data to each Countie and storage it
averageEarningsCounties = asingNumberToTerritories(COUNTIES, averageEarnings)

# ---------FINISH GET AVERAGE EARNINGS --------------

# Calculate the housepriceToIncomeRatio
housepriceToIncomeRatioIndex = \
    gethousepriceToIncomeRatioIndex(housePriceCounties, averageEarningsCounties)

# ----------------------------FINISH HOUSE PRICE TO INCOME RATIO----------------------------

# -------------------------------CALCULATING COST OF LIVING INDEX----------------------------

# Load external data
d = {}
with open("externaldata/numbeoscostOfLivingIndex.txt") as f:
    numbeoscostOfLivingIndex = dict(x.rstrip().split(':', 1) for x in f)

costOfLivingCountiesIndex = asingNumbersToTerritories(COUNTIES, numbeoscostOfLivingIndex)

# ----------------------------FINISH CALCULATING PURCHASING POWER----------------------------

# ----------------------------OBTAIN SAEFTY INDEX -------------------------------------------

# ----------OBTAIN CRIME OFFENCES ------------

# URL of the dataset for crimeOffences
crimeOffences_url = \
    'http://www.cso.ie/StatbankServices/StatbankServices.svc/jsonservice/responseinstance/CJA07'

# Build the Dataset from JsonUrl
crimeOffences_dataset = getDatasetFromJsonUrlWLabel(crimeOffences_url)

# Get the last year we have data
dataset_LastYear = list(crimeOffences_dataset['Year'])[-1]

# Filter the database for year
crimeOffences_data = \
    getDataForVariable(crimeOffences_dataset, 'Year', dataset_LastYear)

# Group data by COUNTIES
crimeOffencesAllCounties = {}
for countie in COUNTIES:
    crimeOffencesAllCounties[countie] = 0
    for data in crimeOffences_data.iterrows():
        if (countie == 'Dublin'):
            if (str(data[1][0].encode('utf-8')).find('D.M.R') > -1):
                crimeOffencesAllCounties[countie] += data[1][4]
        else:
            if (str(data[1][0].encode('utf-8')).find(countie) > -1):
                crimeOffencesAllCounties[countie] += data[1][4]

# Calculate crimes in village match counties
Claremorris = 0
Mayorstone = 0
Kerrykeel = 0
for data in crimeOffences_data.iterrows():
    if (str(data[1][0].encode('utf-8')).find('Claremorris') > -1):
        Claremorris += data[1][4]
    if (str(data[1][0].encode('utf-8')).find('Mayorstone') > -1):
        Mayorstone += data[1][4]
    if (str(data[1][0].encode('utf-8')).find('Kerrykeel') > -1):
        Kerrykeel += data[1][4]

# Fix Shared Divisions
crimeOffencesAllCounties['Carlow'] /= 2
crimeOffencesAllCounties['Kilkenny'] /= 2
crimeOffencesAllCounties['Cavan'] /= 2
crimeOffencesAllCounties['Monaghan'] /= 2
crimeOffencesAllCounties['Laois'] /= 2
crimeOffencesAllCounties['Offaly'] /= 2
crimeOffencesAllCounties['Sligo'] /= 2
crimeOffencesAllCounties['Leitrim'] /= 2
crimeOffencesAllCounties['Roscommon'] /= 2
crimeOffencesAllCounties['Longford'] /= 2

# Extract Claremorris from Clare Countie
crimeOffencesAllCounties['Clare'] -= Claremorris

# Extract Mayorstone from Mayo Countie
crimeOffencesAllCounties['Mayo'] -= Mayorstone

# Extract Kerrykeel from Kerry Countie
crimeOffencesAllCounties['Kerry'] -= Kerrykeel

# ----------FINISH CRIME OFFENCES ------------

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

# OBTAIN Number for linear Correlation from external file
fileLinearCorrelation = open("externaldata/linearcorrelationsafetyIndex.txt")
linearCorrelation = float(fileLinearCorrelation.read())

# Calculation safetyIndex
safetyIndex = {}
for territory in crimeOffencesAllCounties:
    safetyIndex[territory] = linearCorrelation * (crimeOffencesAllCounties[territory] / population[territory])

# ----------------------------FINISH SAEFTY INDEX----------------------------------------------

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

# ----------------------------OBTAIN TRAFFIC TIME INDEX -------------------------------------------

# ----------OBTAIN totalTimeSpend ------------

# URL of the dataset for totalTimeSpend
totalTimeSpend_url = \
    'http://www.cso.ie/StatbankServices/StatbankServices.svc/jsonservice/responseinstance/CD005'

# Build the Dataset from JsonUrl
totalTimeSpend_dataset = getDatasetFromJsonUrlWLabel(totalTimeSpend_url)

# Get the last year we have data
dataset_LastYear = list(totalTimeSpend_dataset['Census Year'])[-1]

# Filter the database for year
totalTimeSpend_data = \
    getDataForVariable(totalTimeSpend_dataset, 'Census Year', dataset_LastYear)

# Filter the database for other variables
totalTimeSpend_dataYearSex = \
    getDataForVariable(totalTimeSpend_data, 'Sex', 'Both sexes')
totalTimeSpend_dataYearSexTime = \
    getDataForVariable(totalTimeSpend_dataYearSex, 'Travelling Time', 'Total time travelling')
totalTimeSpend_dataYearSexTownAge = \
    getDataForVariable(totalTimeSpend_dataYearSexTime, 'At Work School or College', 'Population aged 15 years and over at work')

# Extractig the data
totalTimeSpendAllCounties = {}
for data in totalTimeSpend_dataYearSexTownAge.iterrows():
    totalTimeSpendAllCounties[list(list(data)[1])[1]] = list(list(data)[1])[6]

# Sum population for Tipperary
totalTimeSpendAllCounties['Tipperary'] = totalTimeSpendAllCounties['South Tipperary']\
    + totalTimeSpendAllCounties['North Tipperary']

# Taking only data we need
totalTimeSpend = asingNumbersToTerritories(COUNTIES, totalTimeSpendAllCounties)

# ----------FINISH totalTimeSpend ------------

# OBTAIN Number for linear Correlation from external file
fileLinearCorrelation = open("externaldata/linearcorrelationTrafficTimeIndex.txt")
linearCorrelation = float(fileLinearCorrelation.read())

# Calculation safetyIndex
trafficTimeIndex = {}
for territory in COUNTIES:
    trafficTimeIndex[territory] = linearCorrelation * (totalTimeSpendAllCounties[territory] / population[territory])

# ----------------------------FINISH TRAFFIC TIME INDEX -------------------------------------------

# ------------------------------- OBTAIN POLLUTION INDEX --------------------------------

# URL of the dataset for Air Quality Index
airQualityIndex_url = \
    'http://erc.epa.ie/real-time-air/www/aqindex/aqih_json.php'

# Get the data JsonUrl
with urllib2.urlopen(airQualityIndex_url) as url:
    airQuality = json.loads(url.read().decode())

# Get index for areas
Rural_East = int(airQuality['aqihsummary'][0]['aqih'][0])
Cork_City = int(airQuality['aqihsummary'][1]['aqih'][0])
Rural_West = int(airQuality['aqihsummary'][2]['aqih'][0])
Large_Towns = int(airQuality['aqihsummary'][3]['aqih'][0])
Small_Towns = int(airQuality['aqihsummary'][4]['aqih'][0])
Dublin_City = int(airQuality['aqihsummary'][5]['aqih'][0])

# Calculate index for counties
dublin = ((Rural_East + Small_Towns + Dublin_City) / 3) * 10
cork = ((Rural_West + Small_Towns + Cork_City) / 3) * 10
east = ((Rural_East + Small_Towns + Large_Towns) / 3) * 10
west = ((Rural_West + Small_Towns + Large_Towns) / 3) * 10

# Create a dict with areas
pollutionIndex = {}

eastcounties = {'Carlow', 'Cavan', 'Kildare', 'Kilkenny', 'Laois', 'Longford', 'Louth', 'Meath', 'Monaghan', 'Offaly', 'Tipperary', 'Waterford', 'Westmeath', 'Wexford', 'Wicklow'}

for countie in COUNTIES:
    if (countie == 'Dublin'):
        pollutionIndex[countie] = dublin
    elif (countie == 'Cork'):
        pollutionIndex[countie] = cork
    elif (countie in eastcounties):
        pollutionIndex[countie] = east
    else:
        pollutionIndex[countie] = west

# ------------------------------- FINISH POLLUTION INDEX --------------------------------

# ------------------------------- OBTAIN CLIMATE INDEX --------------------------------

# ----------OBTAIN rainDaysIndex ------------

# URL of the dataset for rainDays
rainDays_url = \
    'http://www.cso.ie/StatbankServices/StatbankServices.svc/jsonservice/responseinstance/MTM01'

# Build the Dataset from JsonUrl
rainDays_dataset = getDatasetFromJsonUrlWLabel(rainDays_url)

# Get the last year we have data
dataset_LastYear = list(rainDays_dataset['Month'])[-1].split('M')[0]

# Filter the database for year
rainDays_data = \
    getDataForIncludeVariable(rainDays_dataset, 'Month', dataset_LastYear)

# Filter the database for Raindays
rainDays_dataYearNumber = \
    getDataForVariable(rainDays_data, 'Statistic', 'Raindays (0.2mm or More) (Number)')

# Getting the weatherStations
rainDaysWeatherStations = list(rainDays_dataYearNumber['Meteorological Weather Station'])
weatherStations = {}
for weatherStation in rainDaysWeatherStations:
    weatherStations[weatherStation] = 0

# Filter the weatherStations to plot
rainDays_databyWeatherStations = {}
for weatherStation in weatherStations:
    data = getDataForVariable(rainDays_dataYearNumber, 'Meteorological Weather Station', weatherStation).values
    for dato in data:
        weatherStations[dato[0]] += dato[3]

# Asing a weather Station for each Countie
belmulletCounties = {'Donegal', 'Galway', 'Leitrim', 'Mayo', 'Sligo'}
cahirciveenCounties = {'Kerry', 'Limerick', 'Tipperary', 'Waterford'}
casementCounties = {'Carlow', 'Kildare', 'Louth', 'Wexford', 'Wicklow'}
rochesCounties = {'Kilkenny', 'Laois'}

# Create a dict with areas
rainDaysCounties = {}
for countie in COUNTIES:
    if (countie == 'Dublin'):
        rainDaysCounties[countie] = weatherStations['Dublin airport']
    elif (countie == 'Cork'):
        rainDaysCounties[countie] = weatherStations['Cork airport']
    elif (countie == 'Clare'):
        rainDaysCounties[countie] = weatherStations['Shannon airport']
    elif (countie in belmulletCounties):
        rainDaysCounties[countie] = weatherStations['Belmullet']
    elif (countie in cahirciveenCounties):
        rainDaysCounties[countie] = weatherStations['Cahirciveen']
    elif (countie in casementCounties):
        rainDaysCounties[countie] = weatherStations['Casement']
    elif (countie in rochesCounties):
        rainDaysCounties[countie] = weatherStations['Roches Point']
    else:
        rainDaysCounties[countie] = weatherStations['Mullingar']

# Looking for the difference to the best possibilitie
rainDaysCounties = diferenceToBest(rainDaysCounties, 182.5)

# Get the final rainDaysIndex
rainDaysIndex = {}
for data in rainDaysCounties:
    rainDaysIndex[data] = rainDaysCounties[data] * 100 / 182.5

# ----------FINISH rainDaysIndex ------------

# ----------OBTAIN sunnyDaysIndex ------------

# URL of the dataset for sunnyDaysIndex
sunnyDays_url = \
    'http://www.cso.ie/StatbankServices/StatbankServices.svc/jsonservice/responseinstance/MTM03'

# Build the Dataset from JsonUrl
sunnyDays_dataset = getDatasetFromJsonUrlWLabel(sunnyDays_url)

# Get the last year we have data
dataset_LastYear = list(sunnyDays_dataset['Month'])[-1].split('M')[0]

# Filter the database for year
sunnyDays_data = \
     getDataForIncludeVariable(sunnyDays_dataset, 'Month', dataset_LastYear)

# Filter the database for Raindays
sunnyDays_dataYearNumber = \
     getDataForVariable(sunnyDays_data, 'Statistic', 'Total Sunshine Hours (Number)')

# Getting the weatherStations
sunnyDaysWeatherStations = list(sunnyDays_dataYearNumber['Meteorological Weather Station'])

weatherStations = {}
for weatherStation in sunnyDaysWeatherStations:
    weatherStations[weatherStation] = 0

# Filter the weatherStations to plot
sunnyDays_databyWeatherStations = {}
for weatherStation in weatherStations:
    data = getDataForVariable(sunnyDays_dataYearNumber, 'Meteorological Weather Station', weatherStation).values
    for dato in data:
        weatherStations[dato[0]] += dato[3]

# Asing a weather Station for each Countie
belmulletCounties = {'Donegal', 'Galway', 'Leitrim', 'Mayo', 'Sligo'}
cahirciveenCounties = {'Kerry', 'Limerick', 'Tipperary', 'Waterford'}
casementCounties = {'Carlow', 'Kildare', 'Louth', 'Wexford', 'Wicklow'}
rochesCounties = {'Kilkenny', 'Laois'}

# Create a dict with areas
sunnyDaysHoursCounties = {}
for countie in COUNTIES:
    if (countie == 'Dublin'):
        sunnyDaysHoursCounties[countie] = weatherStations['Dublin airport']
    elif (countie == 'Cork'):
        sunnyDaysHoursCounties[countie] = weatherStations['Cork airport']
    elif (countie == 'Clare'):
        sunnyDaysHoursCounties[countie] = weatherStations['Shannon airport']
    elif (countie in belmulletCounties):
        sunnyDaysHoursCounties[countie] = weatherStations['Belmullet']
    elif (countie in cahirciveenCounties):
        sunnyDaysHoursCounties[countie] = weatherStations['Cahirciveen']
    elif (countie in casementCounties):
        sunnyDaysHoursCounties[countie] = weatherStations['Casement']
    elif (countie in rochesCounties):
        sunnyDaysHoursCounties[countie] = weatherStations['Roches Point']
    else:
        sunnyDaysHoursCounties[countie] = weatherStations['Mullingar']

# Obtain average in the country
total = 0
count = 0
for countie in sunnyDaysHoursCounties:
    if (not np.isnan(sunnyDaysHoursCounties[countie])):
        total += sunnyDaysHoursCounties[countie]
        count += 1
average = total / count

# Convert from hour to day
sunnyDaysCounties = {}
for countie in sunnyDaysHoursCounties:
    if (not np.isnan(sunnyDaysHoursCounties[countie])):
        sunnyDaysCounties[countie] = sunnyDaysHoursCounties[countie] / 24
    else:
        sunnyDaysCounties[countie] = average / 24

# Looking for the difference to the best possibilitie
sunnyDaysCounties = diferenceToBest(sunnyDaysCounties, 182.5)

# Get the final sunnyDaysIndex
sunnyDaysIndex = {}
for data in sunnyDaysCounties:
    sunnyDaysIndex[data] = sunnyDaysCounties[data] * 100 / 182.5

# ----------FINISH sunnyDaysIndex ------------

# ----------OBTAIN indexTemperature ------------

# URL of the dataset for averageTemperature
averageTemperature_url = \
    'http://www.cso.ie/StatbankServices/StatbankServices.svc/jsonservice/responseinstance/MTM02'

# Build the Dataset from JsonUrl
averageTemperature_dataset = getDatasetFromJsonUrlWLabel(averageTemperature_url)

# Get the last year we have data
dataset_LastYear = list(averageTemperature_dataset['Month'])[-1].split('M')[0]

# Filter the database for year
averageTemperature_data = \
     getDataForIncludeVariable(averageTemperature_dataset, 'Month', dataset_LastYear)

# Filter the database for Raindays
averageTemperature_dataYearNumber = \
     getDataForVariable(averageTemperature_data, 'Statistic', 'Mean Temperature (Degrees C)')

# Getting the weatherStations
averageTemperatureWeatherStations = list(averageTemperature_dataYearNumber['Meteorological Weather Station'])

weatherStations = {}
for weatherStation in averageTemperatureWeatherStations:
    weatherStations[weatherStation] = 0

# Filter the weatherStations to plot
averageTemperatureWeatherStations_databyWeatherStations = {}
for weatherStation in weatherStations:
    data = getDataForVariable(averageTemperature_dataYearNumber, 'Meteorological Weather Station', weatherStation).values
    for dato in data:
        weatherStations[dato[0]] += dato[3]

# Asing a weather Station for each Countie
belmulletCounties = {'Donegal', 'Galway', 'Leitrim', 'Mayo', 'Sligo'}
cahirciveenCounties = {'Kerry', 'Limerick', 'Tipperary', 'Waterford'}
casementCounties = {'Carlow', 'Kildare', 'Louth', 'Wexford', 'Wicklow'}
rochesCounties = {'Kilkenny', 'Laois'}

# Count data from how many month we have
totalData = averageTemperatureWeatherStations.count(list(weatherStations.keys())[0])

# Create a dict with areas
averageTemperatureCounties = {}
for countie in COUNTIES:
    if (countie == 'Dublin'):
        averageTemperatureCounties[countie] = weatherStations['Dublin airport'] / totalData
    elif (countie == 'Cork'):
        averageTemperatureCounties[countie] = weatherStations['Cork airport'] / totalData
    elif (countie == 'Clare'):
        averageTemperatureCounties[countie] = weatherStations['Shannon airport'] / totalData
    elif (countie in belmulletCounties):
        averageTemperatureCounties[countie] = weatherStations['Belmullet'] / totalData
    elif (countie in cahirciveenCounties):
        averageTemperatureCounties[countie] = weatherStations['Cahirciveen'] / totalData
    elif (countie in casementCounties):
        averageTemperatureCounties[countie] = weatherStations['Casement'] / totalData
    elif (countie in rochesCounties):
        averageTemperatureCounties[countie] = weatherStations['Roches Point'] / totalData
    else:
        averageTemperatureCounties[countie] = weatherStations['Mullingar'] / totalData

# Get the final averageTemperatureIndex
averageTemperatureIndex = {}
for data in averageTemperatureCounties:
    averageTemperatureIndex[data] = averageTemperatureCounties[data] * 5

# ----------FINISH indexTemperature ------------

# Obtain the climateIndex
climateIndex = {}
for data in rainDaysIndex:
    climateIndex[data] = (rainDaysIndex[data] + sunnyDaysIndex[data] + averageTemperatureIndex[data]) / 3

# ------------------------------- FINISH CLIMATE INDEX --------------------------------

# ------------------------------- OBTAIN QUALITY OF LIFE INDEX --------------------------------

qualityOfLifeIndex = madeQualityOfLifeIndex(purchasingPowerInclRentIndex,
                                            housepriceToIncomeRatioIndex,
                                            costOfLivingCountiesIndex,
                                            safetyIndex,
                                            healthIndex,
                                            trafficTimeIndex,
                                            pollutionIndex,
                                            climateIndex)


print(qualityOfLifeIndex)

print('Quality of air - Update every hour')

for data in airQuality['aqihsummary']:
    print(data['aqih-region'], ':', data['aqih'])

# ------------------------------- FINISH QUALITY OF LIFE INDEX --------------------------------
