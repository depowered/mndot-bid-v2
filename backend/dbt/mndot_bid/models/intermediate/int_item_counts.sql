with bids as (

    select * from {{ ref('stg_bids') }}

),

counts as (

    select 
        item_id, 
        count(distinct contract_id) as contract_count,
        count(1) as bid_count

    from bids

    group by item_id

)

select * from counts