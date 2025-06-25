-- Creates a date spine with 3000 sequential days starting Jan 1, 2022
WITH date_spine AS (
  SELECT
    DATEADD(day, seq4(), '2022-01-01') AS date_day
  FROM TABLE(GENERATOR(ROWCOUNT => 3000))
)

-- Add useful columns for temporal aggregation
SELECT
  date_day,
  EXTRACT(year FROM date_day) AS year,
  EXTRACT(month FROM date_day) AS month,
  TO_CHAR(date_day, 'YYYY-MM') AS year_month,
  DATE_TRUNC('week', date_day) AS week_start,
  DATE_TRUNC('month', date_day) AS month_start,
  DATE_TRUNC('quarter', date_day) AS quarter_start
FROM date_spine
