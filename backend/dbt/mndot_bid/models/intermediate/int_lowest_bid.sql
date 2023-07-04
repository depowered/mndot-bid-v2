with bidders as (

    select * from {{ ref('stg_bidders') }}

),

lowest_bids as (

    select 
        contract_id, 
        min(bid_total_cents) as lowest_bid_cents

    from bidders

    group by contract_id

),

joined as (

    select 
        bidders.*, 
        lowest_bids.lowest_bid_cents

    from bidders

    left outer join lowest_bids
        on bidders.bid_total_cents = lowest_bids.lowest_bid_cents

    order by bidders.contract_id 

),

renamed as (

    select 
        contract_id, 
        bidder_id,
        bidder_name,
        ifnull(lowest_bid_cents::boolean, false) as lowest_bid

    from joined
)

select * from renamed