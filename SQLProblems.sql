"""
@Author: Prayag Bhoir
@Date: 24-08-2024
@Last Modified by: Prayag Bhoir
@Last Modified time: 4-09-2024
@Title : Sql Problems on Covid dataset
"""
-- 1. Death Percentage Analysis
USE prayagdb
-- a. Global Death Percentage
-- Question: Calculate the global death percentage.
SELECT 
  (SUM(CAST(Deaths AS INT)) * 100.0) / SUM(CAST(Confirmed AS INT)) AS global_death_percentage
FROM 
  country_wise_latest;

-- b. Local Death Percentage
-- Question: Calculate the local death percentage for each country.
SELECT 
  [Country Region] AS Country,
  (SUM(CAST(Deaths AS INT)) * 100.0) / SUM(CAST(Confirmed AS INT)) AS local_death_percentage
FROM 
  country_wise_latest
GROUP BY
  [Country Region]
HAVING
  [Country Region] = 'India';


-- 2. Infected Population Percentage Analysis

-- a. Local Infected Population Percentage
-- Question: Calculate the infected population percentage for each country.
SELECT 
  Country_Region,
  (TotalCases * 100.0 / [Population]) AS Infected_rate
FROM 
  worldometer_data;

-- b. Global Infected Population Percentage
-- Question: Calculate the global infected population percentage.
SELECT
  SUM(TotalCases) AS TotalCase,
  SUM(CAST([Population] AS BIGINT)) AS Population,
  (SUM(TotalCases) * 100.0 / SUM(CAST([Population] AS BIGINT))) AS Global_infected_rate
FROM 
  worldometer_data;


-- 3. Highest Infection Rates by Country
-- Question: Identify the countries with the highest infection rates.
SELECT 
  TOP 10 Country_Region AS country, 
  (SUM(TotalCases) * 100.0) / Population AS infection_rate
FROM 
  worldometer_data
GROUP BY 
  Country_Region, Population
ORDER BY 
  infection_rate DESC;


-- 4. Highest Death Counts by Country and Continent

-- a. Countries with Highest Death Counts
-- Question: Identify the countries with the highest death counts.
SELECT 
  TOP 10 Country_Region AS Countries,
  TotalDeaths AS Death_count
FROM 
  worldometer_data
ORDER BY 
  Death_count DESC;

-- b. Continents with Highest Death Counts
-- Question: Identify the continents with the highest death counts.
SELECT 
  TOP 10 Continent,
  SUM(TotalDeaths) AS Death_count
FROM 
  worldometer_data
WHERE 
  Continent IS NOT NULL
GROUP BY
  Continent
ORDER BY 
  Death_count DESC;


-- 5. Average Number of Deaths by Day

-- a. Countries
-- Question: Calculate the average number of deaths per day for each country.
SELECT 
  TOP 10 [Date],
  AVG(Deaths) AS Average_Deaths
FROM 
  covid_19_clean_complete
GROUP BY
  [Date], Country_Region
ORDER BY 
  Average_Deaths DESC;

-- b. Continents
-- Question: Calculate the average number of deaths per day for each continent.
SELECT 
  TOP 10 WHO_Region,
  [Date],
  AVG(Deaths) AS Average_Deaths
FROM 
  covid_19_clean_complete
GROUP BY
  [Date], WHO_Region
ORDER BY 
  Average_Deaths DESC;


-- 6. Average Cases Divided by Population (Top 10 Countries)
-- Question: Find the top 10 countries with the highest average cases divided by population.
SELECT 
  TOP 10 Country_Region AS Country,	
  AVG((TotalCases * 1.0) / [Population]) AS Avg_Cases_By_Population
FROM 
  worldometer_data
GROUP BY
  Country_Region;


-- 7. Highest Rate of Infection Relative to Population
-- Question: Among the countries with the highest total cases, which have the highest rate of infection relative to population?
SELECT 
  TOP 10 [Country_Region] AS country, 
  TotalCases * 1.0 / [Population] AS Infection_rate
FROM 
  worldometer_data
ORDER BY 
  Infection_rate DESC;
