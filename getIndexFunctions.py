"""All the function used to generate index to quality of life."""

from functions import normalice, normaliceBetweenLimits


def getpurchasingPowerInclRentIndex(purchasingPowerTerritories):
    """Recive a dictionary with a number for each territori an calculate the Purchasing Power."""
    for territory in purchasingPowerTerritories:
        purchasingPowerTerritories[territory] = purchasingPowerTerritories[territory] * 1.65
    return purchasingPowerTerritories


def gethousepriceToIncomeRatioIndex(housePriceIndexTerritories, averageEarningsIndexTerritories):
    """Recive a dictionary with a number for each territori an calculate the Purchasing Power."""
    priceToIncomeRatioTerritories = {}
    for territory in housePriceIndexTerritories:
        priceToIncomeRatioTerritories[territory] = \
            housePriceIndexTerritories[territory] / averageEarningsIndexTerritories[territory]
    return priceToIncomeRatioTerritories


def madeQualityOfLifeIndex(purchasingPowerInclRentIndex,
                           housepriceToIncomeRatio,
                           costOfLivingIndex,
                           safetyIndex,
                           healthIndex,
                           trafficTimeIndex,
                           pollutionIndex,
                           climateIndex):
    """Recive arguments to calculate the Quality of Life index."""
    qualityOfLifeIndex = {}
    for territory in purchasingPowerInclRentIndex:
        qualityOfLifeIndex[territory] = 100 \
            + purchasingPowerInclRentIndex[territory] / 2.5 \
            - (housepriceToIncomeRatio[territory] * 1.0) \
            - costOfLivingIndex[territory] / 5 \
            + safetyIndex[territory] / 2.0 \
            + healthIndex[territory] / 2.5 \
            - trafficTimeIndex[territory] / 2.0 \
            - pollutionIndex[territory] * 2.0 / 3.0 \
            + climateIndex[territory] / 2.0
    return qualityOfLifeIndex

def getsafetyIndex(crimeOffences, popultion, limits):
    """Recive dictionaries with crimeOffences, popultion and limits and calculate Safety Index."""
    # Obtain the crimeOffencesByPopultion
    crimeOffencesByPopultion = {}
    for territory in crimeOffences:
        crimeOffencesByPopultion[territory] = crimeOffences[territory] / popultion[territory]

    # Normalice crimeOffencesByPopultion
    normalice(crimeOffencesByPopultion)

    # Sum min limit to obtain safety index
    safetyIndex = normaliceBetweenLimits(crimeOffencesByPopultion,
                                         float(max(limits.values())), float(min(limits.values())))

    return safetyIndex


def gethealthIndex(healthCareExpenditure, popultion, limits):
    """Recive dictionaries with healthCareExpenditure, popultion and limits and calculate Safety Index."""
    # Obtain the healthCareExpenditureByPopultion
    healthCareExpenditureByPopultion = {}
    for territory in healthCareExpenditure:
        healthCareExpenditureByPopultion[territory] = healthCareExpenditure[territory] / popultion[territory]

    # Normalice healthCareExpenditureByPopultion
    normalice(healthCareExpenditureByPopultion)

    # Sum min limit to obtain safety index
    healthIndex = normaliceBetweenLimits(healthCareExpenditureByPopultion,
                                         float(max(limits.values())), float(min(limits.values())))
                                         
    return healthIndex
