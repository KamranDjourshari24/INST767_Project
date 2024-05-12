## This query combines the first names of F1 racers and EPL players using UNION ALL. Then, it counts the occurrences of each first name and retrieves the top 3 most common first names among them. It provides an interesting insight into the distribution of names among athletes in these two sports.

SELECT 
    First_Name,
    COUNT(*) AS Count
FROM 
    (
        SELECT 
            First_Name
        FROM 
            finalproject.racerf1_country

        UNION ALL

        SELECT 
            firstname
        FROM 
            finalproject.epl_country
    ) AS CombinedNames
GROUP BY 
    First_Name
ORDER BY 
    Count DESC;
