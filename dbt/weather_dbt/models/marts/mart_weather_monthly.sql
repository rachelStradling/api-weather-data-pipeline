{{ config(materialized='view') }}

with daily as (
  select
    city,
    date,
    avg_temp_c,
    max_daytime_wind_speed,
    max_daytime_wind_gust,
    total_precip_mm,
    total_snowfall_mm,
    daytime_hours,
    daytime_clear_hours,
    rain_free_day,
    snow_event_day,
    ropeway_safe_day
  from {{ ref('int_weather_daily') }}
),

aggregated as (
  select
    city,
    date_trunc(date, month) as month_start_date,
    format_date('%Y-%m', date) as year_month,

    count(distinct date) as days_in_month_with_data,

    -- Temperature
    avg(avg_temp_c) as avg_monthly_temp_c,
    min(avg_temp_c) as min_daily_avg_temp_c,
    max(avg_temp_c) as max_daily_avg_temp_c,

    -- Ropeway / wind (day-level, based on daytime wind conditions)
    countif(ropeway_safe_day) as ropeway_safe_days,
    safe_divide(
      countif(ropeway_safe_day),
      count(distinct date)
    ) as ropeway_safe_days_ratio,

    -- Rain metrics
    countif(rain_free_day) as rain_free_days,
    safe_divide(
      countif(rain_free_day),
      count(distinct date)
    ) as rain_free_days_ratio,

    -- Snow metrics
    countif(snow_event_day) as snow_event_days,
    safe_divide(
      countif(snow_event_day),
      count(distinct date)
    ) as snow_event_days_ratio,
    safe_divide(
      sum(total_snowfall_mm),
      nullif(countif(snow_event_day), 0)
    ) as avg_snow_intensity_mm,

    -- Visibility / clear-sky metrics
    sum(daytime_hours) as total_daytime_hours,
    sum(daytime_clear_hours) as total_daytime_clear_hours,
    safe_divide(
      sum(daytime_clear_hours),
      nullif(sum(daytime_hours), 0)
    ) as daytime_clear_sky_hours_ratio

  from daily
  group by
    city,
    month_start_date,
    year_month
)

select *
from aggregated
