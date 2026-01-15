with hourly as (
    select
        city,
        date(timestamp) as forecast_date,
        temperature_c,
        timestamp,
        is_daytime,
        wind_speed_10m,
        wind_gusts_10m,
        precipitation,
        snowfall,
        cloud_cover
    from {{ ref('stg_hourly_forecast') }}
),

day_level as (
    select
        city,
        forecast_date,
		
        -- temperature
        max(temperature_c) as max_temperature,
        min(temperature_c) as min_temperature,
        
        -- wind
        max(case when is_daytime then wind_speed_10m end) as max_daytime_wind_speed,
        max(case when is_daytime then wind_gusts_10m end) as max_daytime_wind_gust,

        -- rain
        sum(precipitation) as total_precip_mm,
        case when sum(precipitation) = 0 then true else false end as rain_free_day,
		sum(snowfall) as total_snowfall_mm,
        case when sum(snowfall) = 0 then true else false end as snow_free_day,
        
        -- visibility
        count(if(is_daytime,1,NULL)) as daytime_hours,
        count(if(is_daytime and cloud_cover < 30,1,NULL)) as clear_daytime_hours,
        safe_divide(
            count(if(is_daytime and cloud_cover < 30,1,NULL)),
            count(if(is_daytime,1,NULL))
        ) as daytime_clear_sky_ratio
    from hourly
    group by city, forecast_date
),

best_vis as (
    select
        city,
        date(timestamp) as forecast_date,
        -- tie-breaker: prefer earliest clear hour with lowest cloud_cover
        array_agg(
          struct(timestamp, cloud_cover)
          order by cloud_cover asc, timestamp asc
        )[offset(0)].timestamp as best_visibility_hour
    from hourly
    where is_daytime
    group by city, forecast_date
)

select
    d.*,
    b.best_visibility_hour
from day_level d
left join best_vis b
  using (city, forecast_date)
