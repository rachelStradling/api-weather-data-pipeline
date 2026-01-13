{{ config(materialized='view') }}

select
  * except(is_daytime),
  safe_cast(sunrise as datetime) as sunrise_dt,
  safe_cast(sunset  as datetime) as sunset_dt,
  datetime(timestamp) as hour_dt,
  case
    when safe_cast(sunrise as datetime) is null
      or safe_cast(sunset  as datetime) is null
      or timestamp is null
    then null
    when datetime(timestamp) >= safe_cast(sunrise as datetime)
     and datetime(timestamp) <  safe_cast(sunset  as datetime)
    then true
    else false
  end as is_daytime
from {{ source('weather', 'hourly_forecast') }}
