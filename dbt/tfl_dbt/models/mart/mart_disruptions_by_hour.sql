with int_data as (
    select * from {{ ref('int_tfl_disruptions') }}
)

select
    hour,
    count(case when severity_category != 'Good' then 1 end) as disrupted_lines,
    count(*) as total_lines
from int_data
group by hour
order by hour desc
