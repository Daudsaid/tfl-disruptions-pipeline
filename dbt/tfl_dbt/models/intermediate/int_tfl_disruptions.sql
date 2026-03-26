with staged as (
    select * from {{ ref('stg_tfl_disruptions') }}
),

aggregated as (
    select
        line_id,
        line_name,
        status,
        severity_category,
        date_trunc('hour', recorded_at) as hour,
        count(*) as readings
    from staged
    group by line_id, line_name, status, severity_category, date_trunc('hour', recorded_at)
)

select * from aggregated
