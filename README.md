This script take data from the open data project of Ireland Goverment and calculate an Quality of life Index for each Counties.

the moment this are the scripts includes

* **purchasingPowerInclRentIndex:** Read directly the json from web. We look for the data of the last year it have. Only have data for State, the I extract it and asing the same number for each countie. Then traet it to achieve the desiree result.  
**Required documents:** This script don't need any external documents

* **housepriceToIncomeRatioIndex:** Read directly the json from web to obtain first the house price. This json don't have information for all counties, only for a few and another for 'Other Areas'. We look first for the data of the last year it have. After this get the results a create a dictionary given to each countie his value, and if the countie doesn't exist asing to it the 'Other Areas' value.
After we get the Average earning from the url of the json. Look for the data of the last year it have. Only have data for State, the I extract it and asing the same number for each countie.
With this two dictonaries I create a new one with the final desiree index.  
**Required documents:**  This script don't need any external documents

* **costOfLivingIndex:** To calculate it we need the Numbeos numbers. We have to obtain it manually. I do it. We only have numbers for a few counties, the I take it an create a file with a standar format. I put in it the data we have and for the ones we don't have number I put in 'Other Areas' the value give for Numbeo to the State. After this get the results a create a dictionary given to each countie his value, and if the countie doesn't exist asing to it the 'Other Areas' value.  
Required documents:
externaldata/numbeoscostOfLivingIndex.txt: Have the Numbeo index for Cost of living for the Counties they have. Also have Other areas index, average of the others, to assign to the other counties

* **safetyIndex:** First of all I need the crimeOffences. We read it directly from url. The data is divided by garda, then we group it for counties. After this we need the population an we read it too from the url. We calculate the ratio for each countie (crimeOffences/population), then nomalize it number an fit it between the limits we have in the external document taken from Numbeo and plus they the limit bellow to obtain the final index.
**Required documents:**
externaldata/limitssafetyIndex.txt: Have the limits to fit the data. In this case I calculate it from the data to Dublin as up and a calculate data to Roscommon.

* **healthIndex:** We read directly the healthCareExpenditure from the url. We obtain a number for all state and we divided it between counties. Then we obtain for each countie healthCareExpenditure/popultion, then nomalize it number an fit it between the limits we have in the external document taken from Numbeo and plus they the limit bellow to obtain the final index.
**Required documents:**
externaldata/limitshealthIndex.txt: Have the limits to fit the data. In this case I take the countries inmeditaly above an bellow to Ireland in Health Care Index for year 2016.

* **trafficTimeIndex:** We read directly the trafficTimeIndex from the url. We obtain a number for each counties. Then we dividen between population to obtain  trafficTimeIndex/popultion, then nomalize it number an fit it between the limits we have in the external document taken from Numbeo and plus they the limit bellow to obtain the final index.  
**Required documents:**
externaldata/limitstrafficTimeIndex.txt:  Have the limits to fit the data. In this case I take the countries inmeditaly above an bellow to Ireland in Traffic Index for year 2017.

* **pollutionIndex:**  We read directly the Air Quality Index from the url of the json manteined by the EPA. We obtain a number for six location and with this we calculate a number for each countie to obtain the final index. This information is updated by the EPA each hour and this make so variable our QualityOfLifeIndex.
**Required documents:** This script don't need any external documents

* **climateIndex:** We read directly the Average Temperature taken in all the Weather Stations and we fit for each counties and to obtain the index calculate the diference between the best possible (20 grades average for the year) and multiply by 5 to put it in an 0-100 scale. Then we obtain a index for Raindays. We read the data from the url, and calculate the diference between the best possible (half of days in a year rainy and half sunny) and put this number between o and 100 to obtain an index. We do the same for the Sunnydays, but in this case we have to calculate before the Sunnydays because we only have hours. Finally, with the three index we calculate a climateIndex adding all and dividing it by 3.
**Required documents:** This script don't need any external documents

With all this data I create a new dictionary with the QualityOfLifeIndex. Whit a similar formula to Numbeo. In our case:

    qualityOfLifeIndex = 100
        + purchasingPowerInclRentIndex / 2.5
        - (housepriceToIncomeRatio  * 1.0)
        - costOfLivingIndex  / 5
        + safetyIndex  / 2.0
        + healthIndex  / 2.5
        - trafficTimeIndex / 2.0
        - pollutionIndex  * 2.0 / 3.0
        + climateIndex / 2.0
