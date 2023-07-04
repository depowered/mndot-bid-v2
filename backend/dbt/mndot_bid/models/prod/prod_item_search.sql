with items as (

    select * from {{ ref('int_spec_year_matrix') }}

),

counts as (

    select * from {{ ref('int_item_counts') }}

),

joined as (

    select 
        items.*, 
        ifnull(counts.contract_count, 0) as contract_count, 
        ifnull(counts.bid_count, 0) as bid_count

    from items

    left join counts on (items.id = counts.item_id)

)

select * from joined