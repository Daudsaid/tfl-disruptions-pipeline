with source as (
    select * from {{ source('tfl_aws', 'tfl_disruptions') }}
),

staged as (
    select
        id,
        line_id,
        line_name,
        status,
        severity,
        recorded_at,
        case
            when severity = 10 then 'Good'
            when severity between 6 and 9 then 'Minor Issues'
            when severity between 1 and 5 then 'Severe Issues'
            else 'Unknown'
        end as severity_category
    from source
)

select * from staged
