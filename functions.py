"""All usual function used by script."""


def getCountieFromCode(code):
    """Recive a code and return the name of the Countie."""
    codeCounties = {'-': 'State',
                    '01': 'Dublin',
                    '02': 'Cork',
                    '03': 'Galway',
                    '04': 'Limerick',
                    '05': 'Waterford',
                    '06': 'Other areas'}
    return codeCounties[code]


def asingNumberToTerritories(territories, number):
    """Recive a list of territories and a number and create a dictionary asing to each territory the number."""
    numeredDictionary = {}
    for territory in territories:
        numeredDictionary[territory] = number
    return numeredDictionary


def asingNumbersToTerritories(territories, numbers):
    """Recive a list of territories and a list of some territories with data and match both."""
    numeredTerritories = {}
    for territory in territories:
        if territory in numbers:
            numeredTerritories[territory] = float(numbers[territory])
        else:
            numeredTerritories[territory] = float(numbers['Other areas'])
    return numeredTerritories


def normalice(dictionary):
    """Normalice between 1 and 0 a dictionary of values."""
    minvalue = min(dictionary.values())
    maxvalue = max(dictionary.values())

    for territory in dictionary:
        dictionary[territory] = (dictionary[territory]-minvalue)/(maxvalue-minvalue)
    return dictionary


def normaliceBetweenLimits(dictionary, up, down):
    """Normalice given limits a dictionary of values."""
    diferenceBetweenLimits = up - down
    for territory in dictionary:
        dictionary[territory] = (diferenceBetweenLimits * dictionary[territory]) + down
    return dictionary


def diferenceToBest(dictionary, best):
    """Normalice given limits a dictionary of values."""
    for territory in dictionary:
        if (dictionary[territory] < best):
            dictionary[territory] = dictionary[territory]
        else:
            dictionary[territory] = best - (dictionary[territory] - best)
    return dictionary
