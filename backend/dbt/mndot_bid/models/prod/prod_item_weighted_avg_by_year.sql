with bids as (

    select *, (quantity * unit_price_cents) as cost_cents
    from {{ ref('prod_bids') }}

),

weighted_avg as (

    select 
        item_id,
        category,
        date_part('year', letting_date) as year,
        ( sum(cost_cents) / sum(quantity) )::bigint as weighted_avg_unit_price_cents

    from bids

    group by item_id, category, letting_date

    order by item_id

),

weighted_avg_by_year as (

    pivot weighted_avg
    on year
    using first(weighted_avg_unit_price_cents)
    order by item_id, category

)

select * from weighted_avg_by_year