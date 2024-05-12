##This query calculates the number of races held each year for each circuit, then calculates the average number of races per year across all years for each circuit. It provides insight into the consistency of race schedules across different circuits.

SELECT 
    Circuit,
    AVG(Num_Races) AS Avg_Races_Per_Year
FROM 
    (
        SELECT 
            Circuit,
            COUNT(*) AS Num_Races
        FROM 
            finalproject.f1_race
        GROUP BY 
            Circuit,
            Year
    ) AS Races_Per_Year
GROUP BY 
    Circuit
ORDER BY 
    Avg_Races_Per_Year DESC;
