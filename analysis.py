import pandas as pd

#data grouped by census region
groupedCR = 'groupedByCensusRegion.txt'

#load and filter data
data = pd.read_csv(groupedCR, delimiter = '\t')
data = data[pd.to_numeric(data['Deaths'], errors='coerce').notnull() & data['Census Region'].notnull()]
data['Deaths'] = data['Deaths'].astype(int)
data['Population'] = data['Population'].astype(int)
data['Crude Rate'] = data['Crude Rate'].astype(float)
#used to calculate detailed crude rates per region
data['Calculated Crude Rate'] = (data['Deaths'] / data['Population']) * 100000


#data grouped by year (2019,2020,2021)
groupedYear = 'groupedYearByYear.txt'

#load and filter data
df = pd.read_csv(groupedYear, delimiter='\t')
df = df.dropna(subset=['Year'])
df['Year'] = df['Year'].astype(int)
df['Deaths'] = df['Deaths'].astype(int)
df['Population'] = df['Population'].astype(int)
df['Crude Rate'] = df['Crude Rate'].astype(float)

#q1: calculate the national average maternal mortality rates during the pandemic

#method 1: simple avg of mortality rate on a year by year
avgMortalitySimple = df['Crude Rate'].mean()

#method 2: weighted avg based on total deaths and population during the pandemic
totalDeaths = df['Deaths'].sum()
totalPopulation = df['Population'].sum()
avgMortalityWeighted = (totalDeaths / totalPopulation) * 100000

#q2: regions with the highest and lowest maternal mortality rates
lowest = data.loc[data['Calculated Crude Rate'].idxmin()]
highest = data.loc[data['Calculated Crude Rate'].idxmax()]

print(f'\n1. The national average maternal mortality rate during the pandemic (simple average of year by year data) was found to be: {avgMortalitySimple:.4f} per 100,000')
print(f'\n1b. The national average maternal mortality rate during the pandemic (weighted average) was found to be: {avgMortalityWeighted:.4f} per 100,000')

print(f'\nThe region with the highest maternal mortality rate in the US during the pandemic was {highest["Census Region"]} with {highest["Calculated Crude Rate"]:.4f} per 100,000')
print(f'\nThe region with the lowest maternal mortality rate in the US during the pandemic was {lowest["Census Region"]} with {lowest["Calculated Crude Rate"]:.4f} per 100,000')

#q3: temporal pattern of maternal mortality rate during the pandemic (compared year by year)

#calculate the percentage change in mortality rate from the previous year
df['Crude Rate Change (%)'] = df['Crude Rate'].pct_change() * 100

#print results
print("\nYearly Change in Maternal Mortality Rate:")
print(df[['Year', 'Crude Rate', 'Crude Rate Change (%)']])

print("\n3. The maternal mortality rate remained the same from 2019 to 2020 while we observed a 100% increase in crude rate from 2020 to 2021")
