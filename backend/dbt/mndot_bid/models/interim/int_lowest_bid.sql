with lowest_bid as (
    select contract_id, min(bid_total_cents) as lowest_bid_cents
    from {{ ref('clean_bidders') }}
    group by contract_id
),

joined as (
    select cb.*, lb.lowest_bid_cents
    from {{ ref('clean_bidders') }} cb
    left outer join lowest_bid lb
    on cb.bid_total_cents = lb.lowest_bid_cents
    order by cb.contract_id 
)

select 
    contract_id, 
    bidder_id,
    ifnull(lowest_bid_cents::boolean, false) as lowest_bid
from joined