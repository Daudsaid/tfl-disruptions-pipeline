with int_data as (
    select * from {{ ref('int_tfl_disruptions') }}
)

select
    line_name,
    severity_category,
    count(*) as total_hours,
    min(hour) as first_seen,
    max(hour) as last_seen
from int_data
group by line_name, severity_category
order by line_name
