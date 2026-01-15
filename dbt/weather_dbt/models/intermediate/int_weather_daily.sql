{% set SAFE_WIND = var('ropeway_safe_wind') %}
{% set SAFE_GUST = var('ropeway_safe_gust') %}

select
  city,
  date(hour_dt) as date,

  -- Temperature
  avg(temperature_c) as avg_temp_c,

  -- Wind (daytime only)
  max(case when is_daytime then wind_speed_10m end) as max_daytime_wind_speed,
  max(case when is_daytime then wind_gusts_10m end) as max_daytime_wind_gust,

  -- Precipitation & snow (whole day)
  sum(precipitation) as total_precip_mm,
  sum(snowfall)      as total_snowfall_mm,

  -- Daytime visibility
  sum(case when is_daytime then 1 else 0 end) as daytime_hours,
  sum(
    case
      when is_daytime and cloud_cover < 30 then 1
      else 0
    end
  ) as daytime_clear_hours,

  -- Daily flags
  case when sum(precipitation) = 0 then true else false end as rain_free_day,
  case when sum(snowfall) > 0      then true else false end as snow_event_day,

  -- Ropeway: safe when *daytime* wind conditions stay under thresholds
  case
    when
      max(case when is_daytime then wind_speed_10m  end) < {{ SAFE_WIND }}
      and
      max(case when is_daytime then wind_gusts_10m end) < {{ SAFE_GUST }}
    then true
    else false
  end as ropeway_safe_day

from {{ ref('stg_hourly_historical') }}
group by
  city,
  date
