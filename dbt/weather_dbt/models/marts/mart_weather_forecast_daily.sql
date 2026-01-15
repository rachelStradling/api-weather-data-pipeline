{% set SAFE_WIND = var('ropeway_safe_wind') %}
{% set SAFE_GUST = var('ropeway_safe_gust') %}
{% set MEDIUM_WIND = var('ropeway_medium_wind') %}
{% set MEDIUM_GUST = var('ropeway_medium_gust') %}

select
    city,
    forecast_date,
    
	# Temperatures
    max_temperature,
    min_temperature,
    
    # Ropeway metrics
    max_daytime_wind_speed,
    max_daytime_wind_gust,

    case
      when max_daytime_wind_speed <= {{ SAFE_WIND }}
       and max_daytime_wind_gust  <= {{ SAFE_GUST }}
        then 'high'
      when max_daytime_wind_speed <= {{ MEDIUM_WIND }}
       and max_daytime_wind_gust  <= {{ MEDIUM_GUST }}
        then 'medium'
      else 'low'
    end as ropeway_open_likelihood,
	
    # Rain / snow metrics
	rain_free_day,
    case
      when rain_free_day then 'no_rain'
      when total_precip_mm < 10 then 'light_rain'
      when total_precip_mm < 25 then 'rainy'
      else 'heavy_rain'
    end as rain_category,
	snow_free_day,
    case
      when snow_free_day then 'no_snow'
      when total_snow_mm < 10 then 'light_snow'
      when total_snow_mm < 100 then 'snowy'
      else 'heavy_snow'
    end as rain_category,
	# Visibility metrics
	daytime_clear_sky_ratio,
    best_visibility_hour,
    case
      when daytime_clear_sky_ratio >= 0.7 then 'good'
      when daytime_clear_sky_ratio >= 0.4 then 'okay'
      else 'poor'
    end as visibility_category

from {{ ref('int_weather_forecast_daily') }}