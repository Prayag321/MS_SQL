"""
@Author: Prayag Bhoir
@Date: 24-08-2024
@Last Modified by: Prayag Bhoir
@Last Modified time: 4-09-2024
@Title : Sql Problems on Joins
"""
--JOINS

CREATE DATABASE covidDB;
USE covidDB

SELECT * FROM [dbo].[covid_19_india]
SELECT * FROM covid_vaccine_statewise
SELECT * FROM [dbo].[StatewiseTestingDetails]
SELECT * FROM worldometer_data

--Using JOINS to combine the covid_deaths and covid_vaccine tables :

--1. To find out the population vs the number of people vaccinated
--TEST CODE
-- SELECT 
--   MAX(Total_Individuals_Vaccinated) as Vaccinated
-- FROM
--   covid_vaccine_statewise
-- GROUP BY 
--   [State]
-- HAVING 
--  [State] ='India'

-- SELECT 
--   Population
-- FROM
--  worldometer_data
-- WHERE Country_Region = 'India'

SELECT 
  'India' AS Country,
  (SELECT 
      MAX(Total_Individuals_Vaccinated) * 100.0 /
      (SELECT Population
       FROM worldometer_data
       WHERE Country_Region = 'India')
    FROM covid_vaccine_statewise
    WHERE State = 'India'
  ) AS Vaccinated

 
--2. To find out the percentage of different vaccine taken by people in a country
SELECT 
  [State],
  ROUND( SUM(Covaxin_Doses_Administered)*100.0/SUM(Total_Doses_Administered), 4) as Covaxin,
  ROUND( SUM(CoviShield_Doses_Administered)*100.0/SUM(Total_Doses_Administered), 4) as CoviShield,
  ROUND( SUM(Sputnik_V_Doses_Administered)*100.0/SUM(Total_Doses_Administered), 4) as Sputnik
FROM
  covid_vaccine_statewise
GROUP BY
  [State]
HAVING 
  [State] != 'India'

--3. To find out percentage of people who took both the doses
SELECT 
  [State],
  ROUND( SUM(Second_Dose_Administered)*100.0/SUM(Total_Individuals_Vaccinated), 4) Take_Both_doses
FROM
  covid_vaccine_statewise
GROUP BY
  [State]