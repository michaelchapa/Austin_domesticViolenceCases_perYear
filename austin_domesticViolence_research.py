import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("austin_domesticViolence_cases.csv")
population = {2003: 1031000, 2004: 1075000, 2005: 1120000, 2006: 1167000, 
              2007: 1216000, 2008: 1268000, 2009: 1321000, 2010: 1377000, 
              2011: 1434000, 2012: 1495000, 2013: 1558000, 2014: 1623000, 
              2015: 1692000, 2016: 1763000, 2017: 1838000, 2018: 1915000, 
              2019: 1985000, 2020: 2053000}
# Remove irrelevant attributes
data.drop(labels = ['Incident Number', 'Highest Offense Code', 
                    'Family Violence', 'Address', 'PRA', 'Census Tract', 
                    'Clearance Status', 'Clearance Date', 'UCR Category', 
                    'Category Description'], axis = 1, inplace = True)

# Get counts by Austin Police Department Sector
zipCounts = []
for zipcode in set(data['Zip Code']):
    zipCounts.append((sector, data.groupby('Zip Code').count()))

# order the data by report date
data['Date'] = pd.to_datetime(data['Report Date'])
data.sort_values('Date', inplace = True, na_position = 'first')

dates = pd.DataFrame(data.groupby(data.Date.dt.year).count())
dates.rename(columns = {"Date": "Count"}, inplace = True)

columnNames = list(dates.columns)
columnNames.remove('Count')
dates.drop(columns = columnNames, inplace = True)

# plot dv cases by year
plt.figure(0)
plt.xlabel("Year")
plt.ylabel("Cases")
plt.title("Austin, TX Domestic Violence cases (2003 - 2020)")
plt.xticks(list(dates.index), rotation = 70)
plt.plot(list(dates.index), list(dates['Count']), color = "red")
plt.show()

# plot dv cases as a proportion of population
countList = list(dates['Count'])
popList = list(population.values())
countRatios = [((100000 * count) /pop) for count, pop \
               in zip(countList, popList)]

plt.figure(1)
plt.xlabel("Year")
plt.ylabel("Cases per 100,000 residents")
plt.title("Austin, TX Domestic Violence cases (2003 - 2020)")
plt.xticks(list(dates.index), rotation = 70)
plt.bar(list(dates.index), countRatios, color = "blue")
plt.show()

###########################

print(zipCounts)