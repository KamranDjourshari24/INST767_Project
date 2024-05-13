## Using the "gdp_country" table within the "finalproject" dataset, create a linear regression with "gdp_change_rate" as the independent variable and "gdp_value" as the dependent variable. 

WITH summary_stats AS (
  SELECT
    AVG(gdp_value) AS avg_gdp_value,
    AVG(gdp_change_rate) AS avg_gdp_change_rate,
    COVAR_POP(gdp_change_rate, gdp_value) AS covar,
    VAR_POP(gdp_change_rate) AS var_gdp_change_rate
  FROM
    finalproject.gdp_country
), regression_params AS (
  SELECT
    covar / var_gdp_change_rate AS slope,
    avg_gdp_value AS avg_gdp_value,
    avg_gdp_change_rate AS avg_gdp_change_rate
  FROM
    summary_stats
)

SELECT
  slope,
  avg_gdp_value - slope * avg_gdp_change_rate AS intercept
FROM
  regression_params;

