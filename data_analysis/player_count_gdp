## Find the corelation between no. of players and the average gdp of the country. Is there any positive/negative relationship

##Answer -After you run the query, based on output -  The positive sign indicates that as player count tends to increase, average GDP also tends to increase slightly.The value of 0.15 suggests that the relationship between player count and average GDP is quite weak.In practical terms, this means that there isn't a strong connection between the number of players in a country and its economic performance, as measured by GDP.

WITH player_gdp_stats AS (
    SELECT 
        epl.country_name AS Country, 
        COUNT(display_name) AS Player_Count,
        AVG(GDP_Value) AS Avg_GDP
    FROM 
        `finalproject.epl_country` epl
    JOIN 
        `finalproject.gdp_country` gdp
    ON 
        epl.birth_year = gdp.year AND epl.country_name = gdp.country_name
    GROUP BY 
        epl.country_name
    ORDER BY 
        Player_Count DESC
)
SELECT 
    CORR(Player_Count, Avg_GDP) AS Correlation
FROM 
    player_gdp_stats;
