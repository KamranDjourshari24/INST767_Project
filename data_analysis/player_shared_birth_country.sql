##This query lists all EPL and F1 players with the same birth country

SELECT 
    Shared_Birth_Country,
    Name,
    Category
FROM (
    SELECT DISTINCT
        rf.Full_Name AS Name,
        rf.Country AS Shared_Birth_Country,
        'F1 Racer' AS Category
    FROM 
        finalproject.racerf1_country rf
    JOIN 
        finalproject.epl_country epl ON rf.Country = epl.country_name

    UNION ALL

    SELECT DISTINCT
        epl.display_name AS Name,
        epl.country_name AS Shared_Birth_Country,
        'EPL Player' AS Category
    FROM 
        finalproject.epl_country epl
    JOIN 
        finalproject.racerf1_country rf ON epl.country_name = rf.Country
) AS CombinedData
ORDER BY Shared_Birth_Country, Category, Name;
