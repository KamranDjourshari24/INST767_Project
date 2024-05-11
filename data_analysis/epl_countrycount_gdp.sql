-- How Many Players are in the Premier League per Country and what is the Average GDP of that country over the years (1980s-Present). 
SELECT epl.country_name AS Country, COUNT(display_name) AS Player_Count,
  CONCAT("$ ", FORMAT("%'.3f", Avg_GDP)) AS Avg_GDP
FROM `finalproject.epl_country` epl
  JOIN (
    SELECT country_name, ROUND(AVG(GDP_Value),2) AS Avg_GDP
    FROM `finalproject.gdp_country` gdp
    WHERE country_name IS NOT NULL AND GDP_Value IS NOT NULL
    GROUP BY country_name
  ) AS gdp
    ON epl.country_name = gdp.country_name
GROUP BY epl.country_name, Avg_GDP
ORDER BY Player_Count DESC, Avg_GDP DESC;

