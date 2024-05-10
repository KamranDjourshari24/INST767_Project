## Find the average age of players from each country and also keep a track of how many players are being considered to calculate average (for each country) in the result.

SELECT 
    epl.country_name AS Country,
    COUNT(*) AS Player_Count,
    AVG(EXTRACT(YEAR FROM CURRENT_DATE()) - birth_year) AS Avg_Age

FROM 
    `finalproject.epl_country` epl
GROUP BY 
    country_name
ORDER BY 
    Player_Count DESC;

