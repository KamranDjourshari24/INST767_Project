##This is a query that identifies the F1 racers who have participated in races held in their birth countries:

SELECT DISTINCT
    racerf1_country.Full_Name AS Racer_Name,
    racerf1_country.Country AS Racer_Country,
    f1_race.Country AS Race_Country,
FROM 
    finalproject.racerf1_country
JOIN 
    finalproject.f1_race ON racerf1_country.iso3 = f1_race.iso3
    AND racerf1_country.Country = f1_race.Country
ORDER BY Racer_Name;